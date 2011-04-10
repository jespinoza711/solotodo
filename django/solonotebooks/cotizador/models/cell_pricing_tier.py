from django.db import models
from . import CellPricing, CellPricingPlan, StoreHasProductEntity, utils

class CellPricingTier(models.Model):
    pricing = models.ForeignKey(CellPricing)
    plan = models.ForeignKey(CellPricingPlan)
    shpe = models.ForeignKey(StoreHasProductEntity, blank = True, null = True)
    cellphone_price = models.IntegerField()
    monthly_quota = models.IntegerField()
    three_month_pricing = models.IntegerField()
    six_month_pricing = models.IntegerField()
    twelve_month_pricing = models.IntegerField()
    
    def pretty_monthly_quota(self):
        return utils.prettyPrice(self.monthly_quota)
        
    def pretty_cellphone_price(self):
        return utils.prettyPrice(self.cellphone_price)
    
    def __unicode__(self):
        return str(self.plan)
        
    def compressed_name(self):
        return self.plan.name
        
    def pretty_print(self):
        result = 'Equipo: ' + str(self.pricing) + '\n'
        result += 'Precio equipo: ' + str(self.cellphone_price) + '\n'
        result += 'Nombre plan: ' + str(self.plan) + '\n'
        result += 'Precio plan: ' + str(self.plan.price) + '\n'
        result += 'Cuota mensual total: ' + str(self.monthly_quota) + '\n'
        return result
        
    def update_prices(self):
        self.three_month_pricing = self.cellphone_price + 3 * self.monthly_quota
        self.six_month_pricing = self.cellphone_price + 6 * self.monthly_quota
        self.twelve_month_pricing = self.cellphone_price + 12 * self.monthly_quota
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['pricing', 'plan']
