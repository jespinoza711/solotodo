# Basic description for keeping track of each model at each store over time
class ProductData:
    def __str__(self):
        return self.custom_name + '\n' + str(self.price) + '\n' + self.url + '\n' + self.comparison_field + '\n'
        
    def __unicode__(self):
        return str(self)
