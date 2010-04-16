class ProductData:
    
    def __init__(self):
        self.custom_name = ''
        self.price = 0
        self.url = ''
        
    def __str__(self):
        return self.custom_name + '\n' + str(self.price) + '\n' + self.url + '\n'
