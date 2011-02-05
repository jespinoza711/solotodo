from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from . import Product

class ProductComment(models.Model):
    validated = models.BooleanField()
    comments = models.TextField()
    date = models.DateField()
    nickname = models.CharField(max_length = 255, null = True, blank = True)
    user = models.ForeignKey(User, null = True, blank = True)
    
    notebook = models.ForeignKey(Product)
    
    def get_product(self):
        return self.notebook
        
    def set_product(self, product):
        self.notebook = product
    
    product = property(get_product, set_product)
    
    def __unicode__(self):
        return 'Comentario de ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook comment'
