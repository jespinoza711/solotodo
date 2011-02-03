from django.db import models

class ProductComparisonList(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    products = models.ManyToManyField('Product')
    
    def __unicode__(self):
        return str(self.products.all())
    
    class Meta:
        app_label = 'cotizador'
