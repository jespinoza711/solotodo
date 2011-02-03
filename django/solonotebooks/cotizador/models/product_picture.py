from django.db import models
from . import Product
from sorl.thumbnail.fields import ImageWithThumbnailsField

class ProductPicture(models.Model):
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (90, 90), },
        extra_thumbnails = {
            'large': {'size': (300, 300)},
        },                                          
        upload_to = '.',
        generate_on_save = True,)
    notebook = models.ForeignKey(Product)
    
    def __unicode__(self):
        return 'Foto de ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook picture'
