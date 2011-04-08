from django.db import models
from . import CellCompany

class CellPricing(models.Model):
    company = models.ForeignKey(CellCompany)
    name = models.CharField(max_length = 255, default = '')
    url = models.CharField(max_length = 255)
    best_tier = models.ForeignKey('CellPricingTier', blank = True, null = True)
    
    def raw_text(self):
        return self.company.raw_text() + ' ' + self.name
    
    def __unicode__(self):
        return str(self.company) + ' - ' + self.name
        
    def update_best_tier(self):
        from . import CellPricingTier
        tiers = self.cellpricingtier_set.all()
        best_price = 999999
        for tier in tiers:
            if tier.six_month_pricing < best_price:
                self.best_tier = tier
                best_price = tier.six_month_pricing
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['company', 'name']
