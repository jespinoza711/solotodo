from django.db import models

class ScreenAspectRatio(models.Model):
    h_value = models.IntegerField()
    v_value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.h_value) + ':' + str(self.v_value)
        
    def raw_text(self):
        return unicode(self)
            
    class Meta:
        app_label = 'cotizador'
