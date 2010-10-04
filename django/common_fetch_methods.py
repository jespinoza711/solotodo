import cairo
import pycha.line
from copy import deepcopy
from datetime import date, datetime
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.utils import *

# Method to write a raw string as a log message
def logMessage(message):
    try:
        today_log = LogEntry.objects.get(date = date.today())
    except LogEntry.DoesNotExist:
        today_log = LogEntry()
        today_log.date = date.today()
        today_log.save()
        
    log_message = LogEntryMessage()
    log_message.logEntry = today_log
    log_message.message = message
    log_message.save()

# Method to log the finding of a new model at a store
def logNewModel(shn):
    logMessage('Nuevo modelo: ' + str(shn) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')

# Method to log the finding of a model that already existed ago, but was deleted    
def logReviveModel(shn):
    logMessage('Modelo restaurado: ' + str(shn)  + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')

# Method to log that a notebook in the DB is once again available
def logReviveNotebook(ntbk):
    logMessage('Notebook restaurado: ' + str(ntbk)  + ' (<a href="/admin/cotizador/notebook/' + str(ntbk.id) + '/">Editar</a>)')
    
# Method to log that a store has pull a model from its website
def logLostModel(shn):
    logMessage('Modelo perdido: ' + str(shn) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')

# Method to log that a notebook in the DB is no longer available
def logLostNotebook(ntbk):
    logMessage('Notebook perdido: ' + str(ntbk) + ' (<a href="/admin/cotizador/notebook/' + str(ntbk.id) + '/">Editar</a>)')
    
# Method to log that a store has changed the price on one of its models
def logChangeModelPrice(shn, oldPrice, newPrice):
    logMessage('Modelo cambia de precio: ' + str(shn) + ' de ' + str(oldPrice) + ' a ' + str(newPrice) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')
    
# Method to log that a notebook in the DB has changed its minimum price among
# the stores that carry it with availability
def logChangeNotebookPrice(ntbk, oldPrice, newPrice):
    logMessage('Notebook cambia de precio: ' + str(ntbk) + ' de ' + str(oldPrice) + ' a ' + str(newPrice) + ' (<a href="/admin/cotizador/notebook/' + str(ntbk.id) + '/">Editar</a>)')
    
'''Method that takes a list of ProductData objects adn the store they came from,
checks whether they already exists, if they do, it checks for price differences,
if not, it is added.  Everything is logged '''
def saveNotebooks(ntbks, s):
    for ntbk in ntbks:
        print 'Guardando ' + str(ntbk)
        print 'Buscando si tiene un registro existente'
        try:
            current_shn = StoreHasNotebook.objects.filter(store = s).get(comparison_field = ntbk.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasNotebook.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            current_shn = StoreHasNotebook()
            current_shn.url = ntbk.url
            current_shn.custom_name = ntbk.custom_name
            current_shn.comparison_field = ntbk.comparison_field
            current_shn.store = s
            current_shn.is_available = True
            current_shn.visitorCount = 0
            current_shn.latest_price = ntbk.price
            current_shn.save()
            logNewModel(current_shn)
        
        print 'Viendo si esta registrado como desaparecido'
        if not current_shn.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            logReviveModel(current_shn)
            current_shn.is_available = True
            
        print 'Guardando estado del notebook en tienda'
        current_shn.save()

        # We keep track of prices for every day, and we need to avoid clashes
        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreNotebookHistory.objects.filter(date = date.today()).filter(registry = current_shn)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreNotebookHistory()
            snh.price = ntbk.price
            snh.date = date.today()
            snh.registry = current_shn
            snh.save()    
    
''' Management method that keeps everything coherent (e.g. updating the price of
the notebooks to the minimum among the stores that carry it, etc)'''
def updateAvailabilityAndPrice():
    print 'Actualizando status de disponibilidad de las tiendas'
    shns = StoreHasNotebook.objects.all()
    for shn in shns:
        print ''
        print str(shn)
        if shn.is_available and not shn.prevent_availability_change:
            print 'Buscando logs de registro'
            last_logs = shn.storenotebookhistory_set.order_by('-date')
            try:    
                last_log = last_logs[0]
                if not last_log.date == (date.today()):
                    print 'Ultimo registro no es de hoy, dejando entrada no disponible'
                    shn.is_available = False
                    logLostModel(shn)
                    shn.save()
                else:
                    print 'Ultimo registro es de hoy, viendo si hay cambios'
                    try:
                        yesterday_log = last_logs[1]
                        if yesterday_log.price != last_log.price:
                            print 'Hubieron cambios de precio, registrando'
                            shn.latest_price = last_log.price
                            shn.save()
                            logChangeModelPrice(shn, yesterday_log.price, last_log.price)
                        else:
                            print 'No hay cambios'
                    except IndexError:
                        pass
            except IndexError:
                pass
        shn.save()
    
    print 'Actualizando precios minimos'
    for notebook in Notebook.objects.all():
        print notebook
        
        new_price = notebook.storehasnotebook_set.all().filter(is_available = True).filter(is_hidden = False).aggregate(Min('latest_price'))['latest_price__min']
        
        if new_price:
            print 'El notebook tiene registros de disponibilidad'
            
            if new_price != notebook.min_price:
                logChangeNotebookPrice(notebook, notebook.min_price, new_price)
                npc = NotebookPriceChange()
                npc.notebook = notebook
                npc.price = new_price
                npc.date = date.today()
                npc.save()
                notebook.min_price = new_price
            
            if not notebook.is_available:
                logReviveNotebook(notebook)

            notebook.is_available = True
        else:
            print 'El notebook no tiene registros de disponibilidad'

            if notebook.is_available:
                 logLostNotebook(notebook)

            notebook.is_available = False
            
        npcs = NotebookPriceChange.objects.filter(notebook = notebook)
        if len(npcs) == 0:
            npc = NotebookPriceChange()
            npc.notebook = notebook
            npc.price = notebook.min_price
            npc.date = date.today()
            npc.save()  
            
        notebook.long_description = notebook.rawText()
        
        
        similar_notebooks = [str(ntbk.id) for ntbk in notebook.findSimilarNotebooks()]
        notebook.similar_notebooks = ','.join(similar_notebooks)
        
        
        notebook.save()
        generateChart(notebook)
        
def getStoreNotebooks(fetch_store):
    try:
        store = Store.objects.get(name = fetch_store.name)
    except Store.DoesNotExist:
        store = Store()
        store.name = fetch_store.name
        store.save()
    try:
        ntbks = fetch_store.getNotebooks()
        saveNotebooks(ntbks, store)
    except:
        print('Error al obtener los notebooks de ' + store.name)
        logMessage('Error al obtener los notebooks de ' + store.name)
        shns = StoreHasNotebook.objects.filter(store = store)
        for shn in shns:
            shn.prevent_availability_change = True
            shn.save()
