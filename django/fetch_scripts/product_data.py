# Basic description for keeping track of each model at each store over time
class ProductData:
    def __init__(self):
        self.custom_name = ''
        self.price = 0
        self.url = ''
        self.comparison_field = ''
        
    def __str__(self):
        return self.custom_name + '\n' + str(self.price) + '\n' + self.url + '\n' + self.comparison_field
