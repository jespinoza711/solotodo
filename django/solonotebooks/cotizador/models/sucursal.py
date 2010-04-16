from django.db import models
from solonotebooks.cotizador.models import City, Store

class Sucursal(models.Model):
    name = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    
    store = models.ForeignKey(Store)
    city = models.ForeignKey(City)
    
    def __unicode__(self):
        return unicode(self.city) + ' - ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Sucursal'
        verbose_name = 'Sucursales'
