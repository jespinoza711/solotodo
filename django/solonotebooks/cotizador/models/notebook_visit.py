from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from solonotebooks.cotizador.models import Notebook

class NotebookVisit(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    notebook = models.ForeignKey(Notebook)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook visit'
