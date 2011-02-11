from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from . import Product

class ProductVisit(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    notebook = models.ForeignKey(Product)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product visit'
