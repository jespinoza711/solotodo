from django.db import models
from . import *

class Motherboard(Product):
    allows_raid = models.BooleanField()
    allows_sli = models.BooleanField()
    allows_cf = models.BooleanField()

    brand = models.ForeignKey(MotherboardBrand)
    chipset = models.ForeignKey(MotherboardChipset)
    format = models.ForeignKey(MotherboardFormat)
    memory_channels = models.ForeignKey(MotherboardMemoryChannel)
    audio_channels = models.ForeignKey(MotherboardAudioChannels)
    
    ports = models.ManyToManyField(MotherboardHasPort)
    video_ports = models.ManyToManyField(MotherboardHasVideoPort, blank = True, null = True)
    memory_types = models.ManyToManyField(MotherboardHasMemoryType)
    card_buses = models.ManyToManyField(MotherboardHasCardBus)
    buses = models.ManyToManyField(MotherboardHasBus)
    power_connectors = models.ManyToManyField(MotherboardHasPowerConnector)
    
    # Interface methods
    
    def update_display_name(self):
        self.display_name = unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        result = super(Motherboard, self).base_raw_text()
        if self.allows_raid:
            result += ' RAID'
        if self.allows_sli:
            result += ' SLI'
        if self.allows_cf:
            result += ' CF CrossFire CrossFireX'
        return result
        
    def load_similar_products(self):
        self.similar_products = ''
        
    @staticmethod
    def get_valid():
        return Motherboard.objects.filter(shp__isnull = False)
        
    def pretty_memory_types(self):
        sub_results = [str(memory_type) for memory_type in self.memory_types.all()]
        return ' / '.join(sub_results)
        
    def pretty_video_ports(self):
        if self.video_ports.all():
            sub_results = [str(video_port) for video_port in self.video_ports.all()]
            return ' / '.join(sub_results)
        else:
            return 'No posee'
        
    def pretty_power_connectors(self):
        sub_results = [str(power_connector) for power_connector in self.power_connectors.all()]
        return ' / '.join(sub_results)
        
    def pretty_sli(self):
        if self.allows_sli:
            return 'Si'
        else:
            return 'No'
            
    def pretty_cf(self):
        if self.allows_cf:
            return 'Si'
        else:
            return 'No'
            
    def pretty_raid(self):
        if self.allows_raid:
            return 'Si'
        else:
            return 'No'
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['display_name']
