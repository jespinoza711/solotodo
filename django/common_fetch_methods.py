import cairo
import pycha.line
from copy import deepcopy
from datetime import date, datetime, timedelta
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.utils import *

# Dynamically loads a class
def import_store(name):
    mod = __import__('fetch_scripts.' + name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

# Method to write a raw string as a log message
def logMessage(message):
    log_message = LogEntryMessage()
    log_message.logEntry, created = LogEntry.objects.get_or_create(date = date.today())
    log_message.message = message
    log_message.save()
    
'''Method that takes a list of ProductData objects adn the store they came from,
checks whether they already exists, if they do, it checks for price differences,
if not, it is added.  Everything is logged '''
def saveNotebooks(ntbks, s):
    for ntbk in ntbks:
        print 'Guardando ' + str(ntbk)
        print 'Buscando si tiene un registro existente'
        try:
            current_shne = StoreHasProductEntity.objects.filter(shn__store = s).get(comparison_field = ntbk.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasProductEntity.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            current_shne = StoreHasProductEntity()
            current_shne.url = ntbk.url
            current_shne.custom_name = ntbk.custom_name
            current_shne.comparison_field = ntbk.comparison_field
            current_shne.shn = None
            current_shne.is_available = True
            current_shne.is_hidden = False
            current_shne.latest_price = ntbk.price
            current_shne.save()
            LogNewModel.new(current_shne).save()
        
        print 'Viendo si esta registrado como desaparecido'
        if not current_shne.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            LogReviveModel.new(current_shne).save()
            current_shne.is_available = True
            
        print 'Guardando estado del notebook en tienda'
        current_shne.save()

        # We keep track of prices for every day, and we need to avoid clashes
        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreNotebookHistory.objects.filter(date = date.today()).filter(registry = current_shne)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreNotebookHistory()
            snh.price = ntbk.price
            snh.date = date.today()
            snh.registry = current_shne
            snh.save()    
        else:
            print 'Hay un registro existente, viendo si hay cambios de precio'
            today_history = today_history[0]
            if today_history.price != ntbk.price:
                print 'Hubo un cambio de precio'
                today_history.price = ntbk.price
                today_history.save()
                current_shne.latest_price = ntbk.price
                current_shne.save()
                
    
''' Management method that keeps everything coherent (e.g. updating the price of
the notebooks to the minimum among the stores that carry it, etc)'''
def updateAvailabilityAndPrice():
    print 'Actualizando status de disponibilidad de las tiendas'
    
    print 'Paso 1: Actualizando StoreHasProductEntities'
    shnes = StoreHasProductEntity.objects.all()
    for shne in shnes:
        print ''
        print str(shne)
        if shne.is_available and shne.shn and not shne.shn.prevent_availability_change:
            print 'Buscando logs de registro'
            last_logs = shne.storenotebookhistory_set.order_by('-date')
            try:    
                last_log = last_logs[0]
                if not last_log.date == (date.today()):
                    print 'Ultimo registro no es de hoy, dejando entrada no disponible'
                    shne.is_available = False
                    LogLostModel.new(shne).save()
                    shne.save()
                else:
                    print 'Ultimo registro es de hoy, viendo si hay cambios'
                    try:
                        yesterday_log = last_logs[1]
                        
                        # The second condition helps when executing the "manual_update" script many times
                        # in a single day, preventing repeated log messages
                        if yesterday_log.price != last_log.price and last_log.price != shne.latest_price:
                            print 'Hubieron cambios de precio, registrando'
                            shne.latest_price = last_log.price
                            shne.save()
                            LogChangeModelPrice.new(shne, yesterday_log.price, last_log.price).save()
                        else:
                            print 'No hay cambios'
                    except IndexError:
                        pass
            except IndexError:
                pass
        shne.save()
        
    print 'Paso 2: Actualizando StoreHasProduct'
    shns = StoreHasProduct.objects.all()
    for shn in shns:
        print shn
        shnes = shn.storehasproductentity_set.filter(is_available = True).filter(is_hidden = False).order_by('latest_price')
        if shnes:
            shn.shne = shnes[0]
        else:
            shn.shne = None
            
        shn.save()
        
    print 'Paso 3: Actualizando Notebook'

    for notebook in Notebook.objects.all():
        print notebook
        
        new_price = notebook.storehasproduct_set.filter(shne__isnull = False).aggregate(Min('shne__latest_price'))['shne__latest_price__min']
        
        if new_price:
            print 'El notebook tiene registros de disponibilidad'
            
            log_price_change = True
            if not notebook.is_available:
                LogReviveNotebook.new(notebook).send_notification_mails()
                log_price_change = False
            
            if new_price != notebook.min_price:
                if log_price_change:
                    LogChangeNotebookPrice.new(notebook, notebook.min_price, new_price).send_notification_mails()
                npc = NotebookPriceChange()
                npc.notebook = notebook
                npc.price = new_price
                npc.date = date.today()
                npc.save()
                notebook.min_price = new_price

            notebook.is_available = True
        else:
            print 'El notebook no tiene registros de disponibilidad'

            if notebook.is_available:
                 LogLostNotebook.new(notebook).send_notification_mails()

            notebook.is_available = False
            
        npcs = NotebookPriceChange.objects.filter(notebook = notebook)
        if len(npcs) == 0:
            npc = NotebookPriceChange()
            npc.notebook = notebook
            npc.price = notebook.min_price
            npc.date = date.today()
            npc.save()  
            
        notebook.long_description = notebook.rawText()
        notebook.update_week_discount()
        notebook.update_week_visits()
        
        #similar_notebooks = [str(ntbk.id) for ntbk in notebook.findSimilarNotebooks()]
        #notebook.similar_notebooks = ','.join(similar_notebooks)
        
        
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
    except Exception, e:
        print('Error al obtener los notebooks de ' + store.name)
        logMessage('Error al obtener los notebooks de ' + store.name + ': ' + str(e))
        shns = StoreHasProduct.objects.filter(store = store)
        for shn in shns:
            shn.prevent_availability_change = True
            shn.save()
