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
    
    def __unicode__(self):
        return unicode(self.line) + self.line.separator + self.name
    
    class Meta:
        app_label = 'cotizador'
