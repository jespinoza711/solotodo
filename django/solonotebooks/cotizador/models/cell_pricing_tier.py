from django.db import models
from . import CellPricing, CellPricingPlan, StoreHasProductEntity

class CellPricingTier(models.Model):
    pricing = models.ForeignKey(CellPricing)
    plan = models.ForeignKey(CellPricingPlan)
    shpe = models.ForeignKey(StoreHasProductEntity, blank = True, null = True)
    cellphone_price = models.IntegerField()
    three_month_pricing = models.IntegerField()
    six_month_pricing = models.IntegerField()
    twelve_month_pricing = models.IntegerField()
    
    def __unicode__(self):
        return str(self.plan)
        
    def pretty_print(self):
        result = 'Precio equipo: ' + str(self.cellphone_price) + '\n'
        result += 'Nombre plan: ' + str(self.plan) + '\n'
        result += 'Precio plan: ' + str(self.plan.price) + '\n'
        return result
        
    def update_prices(self):
        self.three_month_pricing = self.cellphone_price + 3 * self.plan.price
        self.six_month_pricing = self.cellphone_price + 6 * self.plan.price
        self.twelve_month_pricing = self.cellphone_price + 12 * self.plan.price
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['pricing', 'plan']
