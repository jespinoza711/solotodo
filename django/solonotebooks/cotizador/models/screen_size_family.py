from django.db import models

class ScreenSizeFamily(models.Model):
    base_size = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.base_size) + ' - ' + unicode(self.base_size + 0.9) + '"'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Screen size family'
        ordering = ('base_size',)
