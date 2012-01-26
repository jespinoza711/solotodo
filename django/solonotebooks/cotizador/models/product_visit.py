from datetime import date, timedelta
from django.db import models
from django.db.models.aggregates import Count
from django.forms import ModelForm
from django.contrib.auth.models import User
from . import Product

class ProductVisit(models.Model):
    date = models.DateTimeField(auto_now_add = True, db_index=True)
    notebook = models.ForeignKey(Product)
    
    def get_product(self):
        return self.notebook
        
    def set_product(self, product):
        self.notebook = product

    @classmethod
    def get_last_day_visitor_count_for_each_product(cls):
        t = date.today()
        pvs = cls.objects.filter(date__gte = t - timedelta(days=1)).values("notebook").annotate(Count("id")).order_by()
        return dict([[e['notebook'], e['id__count']] for e in pvs])
    
    product = property(get_product, set_product)
    
    def __unicode__(self):
        return 'Visita a ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product visit'
