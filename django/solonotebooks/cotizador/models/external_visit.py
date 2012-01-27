from django.db import models
from django.forms import ModelForm
from store_has_product_entity import StoreHasProductEntity

class ExternalVisit(models.Model):
    date = models.DateField(db_index=True)
    shn = models.ForeignKey(StoreHasProductEntity)
    
    def set_shpe(self, shpe):
        self.shn = shpe
        
    def get_shpe(self, shpe):
        return shn
        
    shpe = property(get_shpe, set_shpe)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.shn)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'External Visit'
