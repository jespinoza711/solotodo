from django.db import models
from . import Product
from utils import prettyPrice

class ProductPriceChange(models.Model):
    price = models.IntegerField()
    date = models.DateField()
    
    notebook = models.ForeignKey(Product)
    
    def __unicode__(self):
        return unicode(self.product) + ' - ' + unicode(self.date) + ' - ' + unicode(self.price)
        
    def prettyRepr(self):
        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                  'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return unicode(self.date.day) + ' de ' + months[self.date.month - 1] + ' de ' + unicode(self.date.year) + ': ' + prettyPrice(self.price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product price change'
