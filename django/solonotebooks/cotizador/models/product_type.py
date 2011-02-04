from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class ProductType(models.Model):
    classname = models.CharField(max_length = 255)
    urlname = models.CharField(max_length = 255)
    displayname = models.CharField(max_length = 255)
    adminurlname = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.classname)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product type'
