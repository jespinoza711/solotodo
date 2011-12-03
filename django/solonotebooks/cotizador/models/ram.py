from django.db import models
from solonotebooks.cotizador.models.product import Product
from solonotebooks.cotizador.models.ram_bus import RamBus
from solonotebooks.cotizador.models.ram_capacity import RamCapacity
from solonotebooks.cotizador.models.ram_latency_cl import RamLatencyCl
from solonotebooks.cotizador.models.ram_latency_tras import RamLatencyTras
from solonotebooks.cotizador.models.ram_latency_trcd import RamLatencyTrcd
from solonotebooks.cotizador.models.ram_latency_trp import RamLatencyTrp
from solonotebooks.cotizador.models.ram_line import RamLine
from solonotebooks.cotizador.models.ram_voltage import RamVoltage

class Ram(Product):
    line = models.ForeignKey(RamLine)
    capacity = models.ForeignKey(RamCapacity)
    bus = models.ForeignKey(RamBus)
    voltage = models.ForeignKey(RamVoltage)
    latency_cl = models.ForeignKey(RamLatencyCl, blank=True, null=True)
    latency_trcd = models.ForeignKey(RamLatencyTrcd, blank=True, null=True)
    latency_trp = models.ForeignKey(RamLatencyTrp, blank=True, null=True)
    latency_tras = models.ForeignKey(RamLatencyTras, blank=True, null=True)
    
    def get_display_name(self):
        return '%s %s (%s | %s)' % (unicode(self.line), self.name, unicode(self.capacity), self.bus.title_display())
        
    def raw_text(self):
        result = super(Ram, self).base_raw_text()
        result += ' ' + unicode(self)
        return result
        
    def load_similar_products(self):
        self.similar_products = ''

    class Meta:
        ordering = ['display_name']
        app_label = 'cotizador'
        
    
