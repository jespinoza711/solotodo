from django.db import models

class ScreenResolution(models.Model):
    horizontal = models.IntegerField()
    vertical = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.horizontal) + ' x ' + unicode(self.vertical)
        
    def rawText(self):
        return unicode(self.horizontal) + ' ' + unicode(self.vertical)
        
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Screen resolution'
        ordering = ('horizontal', 'vertical',)
