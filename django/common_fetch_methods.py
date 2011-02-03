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
    
'''Method that takes a list of ProductData objects and the store they came from,
checks whether they already exists, if they do, it checks for price differences,
if not, it is added.  Everything is logged '''
def saveProducts(ntbks, s):
    for ntbk in ntbks:
        print 'Guardando ' + str(ntbk)
        print 'Buscando si tiene un registro existente'
        try:
            current_shpe = StoreHasProductEntity.objects.filter(shp__store = s).get(comparison_field = ntbk.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasProductEntity.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            current_shpe = StoreHasProductEntity()
            current_shpe.url = ntbk.url
            current_shpe.custom_name = ntbk.custom_name
            current_shpe.comparison_field = ntbk.comparison_field
            current_shpe.shp = None
            current_shpe.is_available = True
            current_shpe.is_hidden = False
            current_shpe.latest_price = ntbk.price
            current_shpe.save()
            LogNewModel.new(current_shpe).save()
        
        print 'Viendo si esta registrado como desaparecido'
        if not current_shpe.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            LogReviveModel.new(current_shpe).save()
            current_shpe.is_available = True
            
        print 'Guardando estado del producto en tienda'
        current_shpe.save()

        # We keep track of prices for every day, and we need to avoid clashes
        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreProductHistory.objects.filter(date = date.today()).filter(registry = current_shpe)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreProductHistory()
            snh.price = ntbk.price
            snh.date = date.today()
            snh.registry = current_shpe
            snh.save()    
        else:
            print 'Hay un registro existente, viendo si hay cambios de precio'
            today_history = today_history[0]
            if today_history.price != ntbk.price:
                print 'Hubo un cambio de precio'
                today_history.price = ntbk.price
                today_history.save()
                current_shpe.latest_price = ntbk.price
                current_shpe.save()
                
    
''' Management method that keeps everything coherent (e.g. updating the price of
the products to the minimum among the stores that carry it, etc)'''
def updateAvailabilityAndPrice():
    print 'Actualizando status de disponibilidad de las tiendas'
    
    print 'Paso 1: Actualizando StoreHasProductEntities'
    shpes = StoreHasProductEntity.objects.all()
    for shpe in shpes:
        print ''
        print str(shpe)
        if shpe.is_available and shpe.shp and not shpe.shp.prevent_availability_change:
            print 'Buscando logs de registro'
            last_logs = shpe.storeproducthistory_set.order_by('-date')
            try:    
                last_log = last_logs[0]
                if not last_log.date == (date.today()):
                    print 'Ultimo registro no es de hoy, dejando entrada no disponible'
                    shpe.is_available = False
                    LogLostEntity.new(shpe).save()
                    shpe.save()
                else:
                    print 'Ultimo registro es de hoy, viendo si hay cambios'
                    try:
                        yesterday_log = last_logs[1]
                        
                        # The second condition helps when executing the "manual_update" script many times
                        # in a single day, preventing repeated log messages
                        if yesterday_log.price != last_log.price and last_log.price != shpe.latest_price:
                            print 'Hubieron cambios de precio, registrando'
                            shpe.latest_price = last_log.price
                            shpe.save()
                            LogChangeModelPrice.new(shpe, yesterday_log.price, last_log.price).save()
                        else:
                            print 'No hay cambios'
                    except IndexError:
                        pass
            except IndexError:
                pass
        shpe.save()
        
    print 'Paso 2: Actualizando StoreHasProduct'
    shps = StoreHasProduct.objects.all()
    for shp in shps:
        print shp
        shpes = shp.storehasproductentity_set.filter(is_available = True).filter(is_hidden = False).order_by('latest_price')
        if shpes:
            shp.shpe = shpes[0]
        else:
            shp.shpe = None
            
        shp.save()
        
    print 'Paso 3: Actualizando Productos'

    for product in Product.objects.all():
        print product
        
        new_price = product.storehasproduct_set.filter(shpe__isnull = False).aggregate(Min('shpe__latest_price'))['shpe__latest_price__min']
        
        if new_price:
            print 'El producto tiene registros de disponibilidad'
            
            log_price_change = True
            if not product.is_available:
                LogReviveProduct.new(product).send_notification_mails()
                log_price_change = False
            
            if new_price != product.min_price:
                if log_price_change:
                    LogChangeProductPrice.new(product, product.min_price, new_price).send_notification_mails()
                npc = ProductPriceChange()
                npc.notebook = product
                npc.price = new_price
                npc.date = date.today()
                npc.save()
                product.min_price = new_price

            product.is_available = True
        else:
            print 'El producto no tiene registros de disponibilidad'

            if product.is_available:
                 LogLostProduct.new(product).send_notification_mails()

            product.is_available = False
            
        npcs = ProductPriceChange.objects.filter(notebook = product)
        if len(npcs) == 0:
            npc = ProductPriceChange()
            npc.notebook = product
            npc.price = product.min_price
            npc.date = date.today()
            npc.save()  
            
        product.long_description = product.raw_text()
        product.update_week_discount()
        product.update_week_visits()
        
        #similar_products = [str(ntbk.id) for ntbk in product.findSimilarProducts()]
        #product.similar_products = ','.join(similar_products)
        
        
        product.save()
        product.generate_chart()
        
def getStoreProducts(fetch_store):
    try:
        store = Store.objects.get(name = fetch_store.name)
    except Store.DoesNotExist:
        store = Store()
        store.name = fetch_store.name
        store.save()
    try:
        ntbks = fetch_store.getProducts()
        saveProducts(ntbks, store)
    except Exception, e:
        print('Error al obtener los productos de ' + store.name)
        logMessage('Error al obtener los productos de ' + store.name + ': ' + str(e))
        shps = StoreHasProduct.objects.filter(store = store)
        for shp in shps:
            shp.prevent_availability_change = True
            shp.save()
