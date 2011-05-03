from solonotebooks.cotizador.models.utils import prettyPrice

# Basic description for keeping track of each model at each store over time
class ProductData:
    def __str__(self):
        try:
            result =  self.custom_name + ' (' + self.ptype + ')' + '\n' + str(self.pretty_price()) + '\n'
        except:
            result = self.custom_name + '\n' + str(self.pretty_price()) + '\n'
        if hasattr(self, 'part_number'):
            result += self.part_number + '\n'
        return result
        
    def __unicode__(self):
        return str(self)
        
    def pretty_price(self):
        return prettyPrice(self.price, spacing = '')
