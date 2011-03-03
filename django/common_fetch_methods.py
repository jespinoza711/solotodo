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
def save_products(products, store):
    for product in products:
        store.save_product(product)
                
    
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
        product.update(send_mails = True)
        
    # Other housekeeping stuff
    VideoCardGpu.update_all_tdmark_scores()
    Processor.update_all_pcmark_scores()
        
def get_store_products(fetch_store, reset_prevent_availability_change = True):
    try:
        store = Store.objects.get(name = fetch_store.name)
    except Store.DoesNotExist:
        store = Store()
        store.name = fetch_store.name
        store.save()
        
    store.set_shpe_prevent_availability_change_flag(False)
        
    try:
        products = fetch_store.get_products()
        save_products(products, store)
    except Exception, e:
        print e
        print('Error al obtener los productos de ' + store.name)
        log_message('Error al obtener los productos de ' + store.name + ': ' + str(e))
        store.set_shpe_prevent_availability_change_flag(True)
