import cairo
import pycha.line
from copy import deepcopy
from datetime import date, datetime, timedelta
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.utils import *

# Method to write a raw string as a log message
def log_message(message):
    log_message = LogEntryMessage()
    log_message.logEntry, created = LogEntry.objects.get_or_create(date = date.today())
    log_message.message = message
    log_message.save()
    
'''Method that takes a list of ProductData objects and the store they came from,
checks whether they already exists, if they do, it checks for price differences,
if not, it is added.  Everything is logged '''
def save_products(products, s):
    for product in products:
        print 'Guardando ' + str(product)
        print 'Buscando si tiene un registro existente'
        try:
            current_shpe = StoreHasProductEntity.objects.get(comparison_field = product.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasProductEntity.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            current_shpe = StoreHasProductEntity()
            current_shpe.url = product.url
            current_shpe.custom_name = product.custom_name
            current_shpe.comparison_field = product.comparison_field
            current_shpe.shp = None
            current_shpe.is_available = True
            current_shpe.is_hidden = False
            current_shpe.latest_price = product.price
            current_shpe.save()
            LogNewEntity.new(current_shpe).save()
        
        print 'Viendo si esta registrado como desaparecido'
        if not current_shpe.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            LogReviveEntity.new(current_shpe).save()
            current_shpe.is_available = True
            
        print 'Guardando estado del producto en tienda'
        current_shpe.save()

        # We keep track of prices for every day, and we need to avoid clashes
        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreProductHistory.objects.filter(date = date.today()).filter(registry = current_shpe)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreProductHistory()
            snh.price = product.price
            snh.date = date.today()
            snh.registry = current_shpe
            snh.save()    
        else:
            print 'Hay un registro existente, viendo si hay cambios de precio'
            today_history = today_history[0]
            if today_history.price != product.price:
                print 'Hubo un cambio de precio'
                today_history.price = product.price
                today_history.save()
                current_shpe.latest_price = product.price
                current_shpe.save()
                
    
''' Management method that keeps everything coherent (e.g. updating the price of
the products to the minimum among the stores that carry it, etc)'''
def update_availability_and_price():
    print 'Actualizando status de disponibilidad de las tiendas'
    
    print 'Paso 1: Actualizando StoreHasProductEntities'
    shpes = StoreHasProductEntity.objects.all()
    for shpe in shpes:
        shpe.update()
        
    print 'Paso 2: Actualizando StoreHasProduct'
    for shp in StoreHasProduct.objects.all():
        shp.update()
        
    print 'Paso 3: Actualizando Productos'

    for product in Product.objects.all():
        product.update()
        
    # Other housekeeping stuff
    VideoCardGpu.update_all_tdmark_scores()
    Processor.update_all_pcmark_scores()
        
def get_store_products(fetch_store):
    try:
        store = Store.objects.get(name = fetch_store.name)
    except Store.DoesNotExist:
        store = Store()
        store.name = fetch_store.name
        store.save()
    try:
        products = fetch_store.get_products()
        save_products(products, store)
    except Exception, e:
        print e
        print('Error al obtener los productos de ' + store.name)
        log_message('Error al obtener los productos de ' + store.name + ': ' + str(e))
        shps = StoreHasProduct.objects.filter(store = store)
        for shp in shps:
            shp.prevent_availability_change = True
            shp.save()
