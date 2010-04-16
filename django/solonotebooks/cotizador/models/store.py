from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField

class Store(models.Model):
    name = models.CharField(max_length = 255)
    url = models.URLField()
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (140, 90), },                                          
        upload_to = 'store_logos',
        generate_on_save = True,)
    
    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store'
