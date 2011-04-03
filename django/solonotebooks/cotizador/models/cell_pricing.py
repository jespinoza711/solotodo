from django.db import models
from . import CellCompany

class CellPricing(models.Model):
    company = models.ForeignKey(CellCompany)
    name = models.CharField(max_length = 255, default = '')
    url = models.CharField(max_length = 255)
    
    def raw_text(self):
        return self.company.raw_text() + ' ' + self.name
    
    def __unicode__(self):
        return str(self.company) + ' - ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['company', 'name']
