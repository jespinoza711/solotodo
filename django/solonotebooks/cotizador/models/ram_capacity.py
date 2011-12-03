from django.db import models
from solonotebooks.cotizador.models.ram_dimm_capacity import RamDimmCapacity
from solonotebooks.cotizador.models.ram_dimm_quantity import RamDimmQuantity
from solonotebooks.cotizador.models.ram_total_capacity import RamTotalCapacity

class RamCapacity(models.Model):
    dimm_quantity = models.ForeignKey(RamDimmQuantity)
    dimm_capacity = models.ForeignKey(RamDimmCapacity)
    total_capacity = models.ForeignKey(RamTotalCapacity)
    
    def __unicode__(self):
        return '%s x %s' % (unicode(self.dimm_quantity), unicode(self.dimm_capacity))
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['dimm_quantity', 'dimm_capacity']
