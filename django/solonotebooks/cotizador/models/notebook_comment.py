from django.db import models
from django.forms import ModelForm
from solonotebooks.cotizador.models import Notebook

class NotebookComment(models.Model):
    validated = models.BooleanField()
    ip_address = models.IPAddressField()
    comments = models.TextField()
    date = models.DateField()
    nickname = models.CharField(max_length = 255)
    
    notebook = models.ForeignKey(Notebook)
    
    def __unicode__(self):
        return 'Comentario de ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook comment'
