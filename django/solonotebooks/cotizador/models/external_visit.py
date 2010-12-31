from django.db import models
from django.forms import ModelForm
from store_has_notebook_entity import StoreHasNotebookEntity

class ExternalVisit(models.Model):
    date = models.DateField()
    
    shn = models.ForeignKey(StoreHasNotebookEntity)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.shn)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'External Visit'
