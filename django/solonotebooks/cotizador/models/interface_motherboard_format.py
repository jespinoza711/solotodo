from django.db import models

class InterfaceMotherboardFormat(models.Model):
    name = models.CharField(max_length = 255)
    width = models.IntegerField()
    height = models.IntegerField()
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
