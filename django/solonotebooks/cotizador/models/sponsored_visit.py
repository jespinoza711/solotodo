from django.db import models
from django.forms import ModelForm
from store_has_product import StoreHasProduct

class SponsoredVisit(models.Model):
    date = models.DateField(auto_now_add = True)
    shp = models.ForeignKey(StoreHasProduct)

    def __unicode__(self):
        return '{0} - {1}'.format(self.shp, self.date)
    
    class Meta:
        ordering = ['-date']
        app_label = 'cotizador'
