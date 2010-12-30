from django.db import models
from django.forms import ModelForm
from solonotebooks.cotizador.models import StoreHasNotebook

class ExternalVisit(models.Model):
    date = models.DateField()
    
    shn = models.ForeignKey(StoreHasNotebook)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.shn)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'External Visit'
