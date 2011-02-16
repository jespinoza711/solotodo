from django.db import models
from . import *

class Processor(Product):
    pcmark_id = models.CharField(max_length = 255)

    frequency = models.IntegerField()
    tdp = models.IntegerField()
    min_voltage = models.IntegerField()
    max_voltage = models.IntegerField()
    pcmark_05_score = models.IntegerField()
    pcmark_vantage_score = models.IntegerField()
    passmark_score = models.IntegerField()
    
    is_64_bit = models.BooleanField()
    has_vt = models.BooleanField()
    has_smp = models.BooleanField()
    
    l1_cache = models.ForeignKey(ProcessorL1Cache)
    l2_cache = models.ForeignKey(ProcessorL2Cache)
    l3_cache = models.ForeignKey(ProcessorL3Cache)
    line = models.ForeignKey(ProcessorLine)
    socket = models.ForeignKey(ProcessorSocket)
    core_count = models.ForeignKey(ProcessorCoreCount)
    core = models.ForeignKey(ProcessorCore)
    multiplier = models.ForeignKey(ProcessorMultiplier)
    fsb = models.ForeignKey(ProcessorFsb)
    turbo_modes = models.CommaSeparatedIntegerField(max_length = 50)
    
    # Interface methods
    
    def __unicode__(self):
        return unicode(self.line) + self.line.separator + self.name
        
    def pretty_display(self):
        return unicode(self)
        
    def raw_text(self):
        result = 'Procesador CPU'
        result += ' ' + self.name
        result += ' ' + str(self.frequency)
        if self.is_64_bit:
            result += ' 64-bit 64 bit bits'
        if self.has_vt:
            result += ' virtualization virtualizacion VT'
        if self.has_smp:
            result += ' smp simultaneous multi processing hyper threading hyperthreading hyper-threading HT'
        result += ' ' + self.l1_cache.raw_text()
        result += ' ' + self.l2_cache.raw_text()
        result += ' ' + self.l3_cache.raw_text()
        result += ' ' + self.socket.raw_text()
        result += ' ' + self.line.raw_text()
        result += ' ' + self.core_count.raw_text()
        result += ' ' + self.core.raw_text()
        result += ' ' + self.multiplier.raw_text()
        result += ' ' + self.fsb.raw_text()
            
        return result
        
    def load_similar_products(self):
        threshold = 4
        processors = Processor.get_valid().filter(~Q(id = self.id)).order_by('?')[:threshold]
        self.similar_products = ','.join([str(processor.id) for processor in processors])
        
    @staticmethod
    def get_valid():
        return Processor.objects.filter(is_available = True)
    
    def clone_product(self):
        clone_prod = super(Processor, self).clone_product()

        clone_prod.save()
        return clone_prod
    
    class Meta:
        app_label = 'cotizador'
