from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from solonotebooks.cotizador.models import Product

class NotebookComment(models.Model):
    validated = models.BooleanField()
    comments = models.TextField()
    date = models.DateField()
    nickname = models.CharField(max_length = 255, null = True, blank = True)
    user = models.ForeignKey(User, null = True, blank = True)
    
    notebook = models.ForeignKey(Product)
    
    def __unicode__(self):
        return 'Comentario de ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook comment'
