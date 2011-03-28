from solonotebooks.cotizador.models.utils import prettyPrice

# Basic description for keeping track of each model at each store over time
class ProductData:
    def __str__(self):
        try:
            return self.custom_name + ' (' + self.ptype + ')' + '\n' + str(self.pretty_price()) + '\n'
        except:
            return self.custom_name + '\n' + str(self.pretty_price()) + '\n'
        
    def __unicode__(self):
        return str(self)
        
    def pretty_price(self):
        return prettyPrice(self.price, spacing = '')
