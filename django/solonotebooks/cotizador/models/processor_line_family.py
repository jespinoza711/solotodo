from django.db import models
from solonotebooks.cotizador.models import ProcessorBrand
from sorl.thumbnail.fields import ImageWithThumbnailsField

class ProcessorLineFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(ProcessorBrand)
    text = models.TextField()
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (300, 300), },             
        upload_to = 'processor_line',
        generate_on_save = True,)
    
    def __unicode__(self):
        return self.brand.name + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor line family'
        ordering = ['brand', 'name']
