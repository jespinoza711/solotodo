from django.db import models
from solonotebooks.cotizador.models import InterfaceCardBusName, InterfaceCardBusLane, InterfaceCardBus

class VideoCardBus(models.Model):
    name = models.ForeignKey(InterfaceCardBusName)
    lane = models.ForeignKey(InterfaceCardBusLane)
    version = models.DecimalField(max_digits = 2, decimal_places = 1)
    bus = models.ForeignKey(InterfaceCardBus)
    
    def __unicode__(self):
        str_name = unicode(self.name) 
        if self.name.show_version_and_lanes:
            str_name += ' '
            if str(self.version) != '1.0':
                str_name += str(self.version) + ' ' 
            str_name += unicode(self.lane)
        return str_name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card bus'
        ordering = ['name', 'version', 'lane']
