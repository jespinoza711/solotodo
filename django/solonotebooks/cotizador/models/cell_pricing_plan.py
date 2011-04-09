from django.db import models
from . import CellCompany, utils

class CellPricingPlan(models.Model):
    company = models.ForeignKey(CellCompany)
    name = models.CharField(max_length = 255)
    price = models.IntegerField()
    ordering = models.IntegerField(default = 2)
    includes_data = models.BooleanField()
    
    @classmethod
    def new(self, plan_data, cell_company):
        cpp = CellPricingPlan()
        cpp.company = cell_company
        cpp.name = plan_data[0]
        cpp.price = plan_data[1]
        cpp.includes_data = plan_data[2]
        return cpp
    
    def __unicode__(self):
        return 'Plan ' + self.name
        
    def pretty_price(self):
        return utils.prettyPrice(self.price)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['ordering', 'id']
