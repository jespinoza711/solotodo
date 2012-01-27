from solonotebooks.cotizador.models import *
    
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
        pvs = ProductVisit.get_last_day_visitor_count_for_each_product()
        product.update(product_visits=pvs)
        
    # Other housekeeping stuff
    for ptype in ProductType.objects.all():
        ptype.get_class().custom_update()
