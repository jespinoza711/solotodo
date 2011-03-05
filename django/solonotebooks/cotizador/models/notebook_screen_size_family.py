from django.db import models

class NotebookScreenSizeFamily(models.Model):
    base_size = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.base_size) + '"'
        
    def titleText(self):
        return unicode(self.base_size) + ' a ' + unicode(self.base_size + 0.9) + ' pulgadas'
        
    def raw_text(self):
        return unicode(self.base_size)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook screen size family'
        ordering = ('base_size',)
