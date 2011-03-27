# Basic description for keeping track of each model at each store over time
class ProductData:
    def __str__(self):
        return self.custom_name + ' (' + self.ptype + ')' + '\n' + str(self.price) + '\n'
        
    def __unicode__(self):
        return str(self)
