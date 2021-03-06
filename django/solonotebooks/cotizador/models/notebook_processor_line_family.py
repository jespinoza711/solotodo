from django.db import models
from . import NotebookProcessorBrand
from sorl.thumbnail.fields import ImageWithThumbnailsField

class NotebookProcessorLineFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookProcessorBrand)
    text = models.TextField()
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (300, 300), },             
        upload_to = 'processor_line',
        generate_on_save = True,)
        
    def raw_text(self):
        result = self.brand.raw_text()
        if self.id == 1:
            result += ' netbook'
        if self.id in [2, 11]:
            result += ' subnetbook ultraportatil'
        return result
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor line family'
        ordering = ['brand', 'name']
