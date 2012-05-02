from django.db import models
from solonotebooks.cotizador.models.computer_case_brand import ComputerCaseBrand
from solonotebooks.cotizador.models.computer_case_fan_distribution import ComputerCaseFanDistribution
from solonotebooks.cotizador.models.computer_case_motherboard_format import ComputerCaseMotherboardFormat
from solonotebooks.cotizador.models.computer_case_power_supply import ComputerCasePowerSupply
from solonotebooks.cotizador.models.computer_case_power_supply_position import ComputerCasePowerSupplyPosition
from solonotebooks.cotizador.models.product import Product

class ComputerCase(Product):
    external_5_1_4_bays = models.IntegerField()
    internal_3_1_2_bays = models.IntegerField()
    external_3_1_2_bays = models.IntegerField()
    internal_2_1_2_bays = models.IntegerField()
    rear_expansion_slots = models.IntegerField()
    front_usb_ports = models.IntegerField()
    length = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    weight = models.IntegerField()

    has_front_audio_ports = models.BooleanField(default=True)
    has_front_esata_port = models.BooleanField()
    has_front_firewire_port = models.BooleanField()
    has_motherboard_tray = models.BooleanField()

    brand = models.ForeignKey(ComputerCaseBrand)
    largest_motherboard_format = models.ForeignKey(ComputerCaseMotherboardFormat)
    power_supply = models.ForeignKey(ComputerCasePowerSupply)
    power_supply_position = models.ForeignKey(ComputerCasePowerSupplyPosition)

    frontal_fan_slots = models.ManyToManyField(ComputerCaseFanDistribution, related_name='ffs', blank=True, null=True)
    rear_fan_slots = models.ManyToManyField(ComputerCaseFanDistribution, related_name='rfs', blank=True, null=True)
    side_fan_slots = models.ManyToManyField(ComputerCaseFanDistribution, related_name='sfs', blank=True, null=True)
    top_fan_slots = models.ManyToManyField(ComputerCaseFanDistribution, related_name='tfs', blank=True, null=True)
    bottom_fan_slots = models.ManyToManyField(ComputerCaseFanDistribution, related_name='bfs', blank=True, null=True)
    included_fans = models.ManyToManyField(ComputerCaseFanDistribution, related_name='if', blank=True, null=True)
    
    # Interface methods
    
    def get_display_name(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        result = super(ComputerCase, self).base_raw_text()
        return result
        
    def load_similar_products(self):
        self.similar_products = ''

    class Meta:
        app_label = 'cotizador'
        ordering = ['display_name']
