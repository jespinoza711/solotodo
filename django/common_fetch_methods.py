from solonotebooks.cotizador.models import *
from django.db.models import Min
from datetime import date, datetime

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

def logNewNotebook(shn):
    logMessage('Nuevo modelo: ' + str(shn) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')
    
def logReviveNotebook(shn):
    logMessage('Modelo restaurado: ' + str(shn)  + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')
    
def logLostNotebook(shn):
    logMessage('Modelo perdido: ' + str(shn) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')
    
def logChangeModelPrice(shn, oldPrice, newPrice):
    logMessage('Modelo cambia de precio: ' + str(shn) + ' de ' + str(oldPrice) + ' a ' + str(newPrice) + ' (<a href="' + shn.url + '">Link</a>) (<a href="/admin/cotizador/storehasnotebook/' + str(shn.id) + '/">Editar</a>)')
    
def logChangeNotebookPrice(ntbk, oldPrice, newPrice):
    logMessage('Notebook cambia de precio: ' + str(ntbk) + ' de ' + str(oldPrice) + ' a ' + str(newPrice) + ' (<a href="/admin/cotizador/notebook/' + str(ntbk.id) + '/">Editar</a>)')
    
def saveNotebooks(ntbks, s):
    for ntbk in ntbks:
        print 'Guardando ' + str(ntbk)
        print 'Buscando si tiene un registro existente'
        try:
            current_shn = StoreHasNotebook.objects.filter(store = s).get(custom_name = ntbk.custom_name)
            print 'Si tiene registro existente, usandolo'
        except StoreHasNotebook.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            current_shn = StoreHasNotebook()
            current_shn.url = ntbk.url
            current_shn.custom_name = ntbk.custom_name
            current_shn.store = s
            current_shn.is_available = True
            current_shn.visitorCount = 0
            current_shn.latest_price = ntbk.price
            current_shn.save()
            logNewNotebook(current_shn)
        
        print 'Viendo si esta registrado como desaparecido'
        if not current_shn.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            logReviveNotebook(current_shn)
            current_shn.is_available = True
            
        print 'Guardando estado del notebook en tienda'
        current_shn.save()

        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreNotebookHistory.objects.filter(date = date.today()).filter(registry = current_shn)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreNotebookHistory()
            snh.price = ntbk.price
            snh.date = date.today()
            snh.registry = current_shn
            snh.save()
            
def analyzeStore(p):
    try:
        s = Store.objects.get(name = p.name)
    except Store.DoesNotExist:
        s = Store()
        s.name = p.name
        s.save()
        
    ntbks = p.getNotebooks()
    saveNotebooks(ntbks, s)
    
def updateAvailabilityAndPrice():
    print 'Actualizando status de disponibilidad de las tiendas'
    shns = StoreHasNotebook.objects.all()
    for shn in shns:
        print ''
        print str(shn)
        if shn.is_available:
            print 'Buscando logs de registro'
            last_logs = shn.storenotebookhistory_set.order_by('-date')
            last_log = last_logs[0]
            if not last_log.date == (date.today()):
                print 'Ultimo registro no es de hoy, dejando entrada no disponible'
                shn.is_available = False
                logLostNotebook(shn)
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
    
    print 'Actualizando precios minimos'
    for notebook in Notebook.objects.all():
        print notebook
        new_price = notebook.storehasnotebook_set.all().filter(is_available = True).aggregate(Min('latest_price'))['latest_price__min']
        
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
            
            notebook.is_available = True
        else:
            print 'El notebook no tiene registros de disponibilidad'
            notebook.is_available = False
        
        notebook.save()
