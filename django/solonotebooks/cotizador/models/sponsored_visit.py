from django.db import models
from django.forms import ModelForm
from store_has_product import StoreHasProduct

class SponsoredVisit(models.Model):
    date = models.DateField(auto_now_add = True)
    shp = models.ForeignKey(StoreHasProduct)

    def __unicode__(self):
        return 'Visita a ' + unicode(self.shp)
    
    class Meta:
        app_label = 'cotizador'
