from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks.cotizador.models import Notebook, Store
from utils import prettyPrice

class StoreHasNotebook(models.Model):
    url = models.TextField()
    custom_name = models.CharField(max_length = 255)
    is_available = models.BooleanField()
    prevent_availability_change = models.BooleanField()
    is_hidden = models.BooleanField()
    visitorCount = models.IntegerField()
    latest_price = models.IntegerField()
    comparison_field = models.TextField()    
    
    notebook = models.ForeignKey(Notebook, null = True, blank = True)
    store = models.ForeignKey(Store)
    
    def __unicode__(self):
        return unicode(self.store) + ' - ' + self.custom_name
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has notebook' 
