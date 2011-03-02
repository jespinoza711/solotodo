from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField

class Store(models.Model):
    name = models.CharField(max_length = 255)
    classname = models.CharField(max_length = 255)
    url = models.URLField()
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (140, 90), },                                          
        upload_to = 'store_logos',
        generate_on_save = True,)
    
    def __unicode__(self):
        return unicode(self.name)
        
    def save_product(self, product):
        from . import StoreHasProductEntity
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
            shpe.save()
            LogNewEntity.new(shpe).save()
            
        shpe.update_with_product(product)
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
        verbose_name = 'Store'
