from django.db import models
from django.forms import ModelForm
from store_has_product_entity import StoreHasProductEntity

class ExternalVisit(models.Model):
    date = models.DateField()
    
    shn = models.ForeignKey(StoreHasProductEntity)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.shn)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'External Visit'
