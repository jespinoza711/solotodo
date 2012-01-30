from django.db import models
from . import Product, PowerSupplyPower, PowerSupplyLine, PowerSupplyCertification, PowerSupplyHasPowerConnector, PowerSupplySize

class PowerSupply(Product):
    line = models.ForeignKey(PowerSupplyLine)
    power = models.ForeignKey(PowerSupplyPower)
    certification = models.ForeignKey(PowerSupplyCertification)
    size = models.ForeignKey(PowerSupplySize)

    is_modular = models.BooleanField()
    has_active_pfc = models.BooleanField()

    currents_on_12V_rails = models.CommaSeparatedIntegerField(max_length=255)
    currents_on_5V_rails = models.CommaSeparatedIntegerField(max_length=255)
    currents_on_33V_rails = models.CommaSeparatedIntegerField(max_length=255)

    power_connectors = models.ManyToManyField(PowerSupplyHasPowerConnector)

    def pretty_currents_on_12V_rails(self):
        return PowerSupply.pretty_currents(self.currents_on_12V_rails)

    def pretty_currents_on_5V_rails(self):
        return PowerSupply.pretty_currents(self.currents_on_5V_rails)

    def pretty_currents_on_33V_rails(self):
        return PowerSupply.pretty_currents(self.currents_on_33V_rails)

    @staticmethod
    def pretty_currents(string_value):
        if string_value == '0':
            return 'Desconocido'

        result = []
        for part in string_value.split(','):
            result.append(part + 'A')

        return ' / '.join(result)
    
    def get_display_name(self):
        return '%s %s (%s)' % (unicode(self.line), self.name, unicode(self.power))
        
    def raw_text(self):
        result = super(PowerSupply, self).base_raw_text()
        result += ' ' + unicode(self)
        if self.is_modular:
            result += ' modular'
        if self.has_active_pfc:
            result += ' PFC activo'
        return result
        
    def load_similar_products(self):
        self.similar_products = ''

    class Meta:
        ordering = ['display_name']
        app_label = 'cotizador'