from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField

class Store(models.Model):
    name = models.CharField(max_length = 255)
    classname = models.CharField(max_length = 255)
    url = models.URLField()
    sponsor_cap = models.IntegerField(default = 0)
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (140, 90), },                                          
        upload_to = 'store_logos',
        generate_on_save = True,)
    
    def __unicode__(self):
        return unicode(self.name)
        
    def fetch_product_data(self, url):
        from solonotebooks.fetch_scripts import *
        from . import StoreHasProductEntity
        fetch_store = eval(self.classname + '()')
        product = fetch_store.retrieve_product_data(url)
        if not product:
            return None
        else:
            shpes = StoreHasProductEntity.objects.filter(custom_name = product.custom_name, store = self)
            if shpes:
                return shpes[0]
            else:
                return None
        
    def save_product(self, product):
        from . import StoreHasProductEntity, LogNewEntity, ProductType
        print 'Guardando ' + str(product)
        print 'Buscando si tiene un registro existente'
        try:
            shpe = StoreHasProductEntity.objects.get(comparison_field = product.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasProductEntity.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            shpe = StoreHasProductEntity()
            shpe.url = product.url
            shpe.custom_name = product.custom_name
            shpe.comparison_field = product.comparison_field
            shpe.shp = None
            shpe.is_available = True
            shpe.is_hidden = False
            shpe.latest_price = product.price
            shpe.store = self
            try:
                ptype = ProductType.objects.get(classname = product.ptype)
                shpe.ptype = ptype
            except:
                pass
            shpe.save()
            LogNewEntity.new(shpe).save()
            
        shpe.update_with_product(product)
        
    def set_shpe_prevent_availability_change_flag(self, flag):
        from . import StoreHasProductEntity
        shpes = StoreHasProductEntity.objects.filter(store = self)
        for shpe in shpes:
            shpe.prevent_availability_change = flag
            shpe.save()
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
        verbose_name = 'Store'
