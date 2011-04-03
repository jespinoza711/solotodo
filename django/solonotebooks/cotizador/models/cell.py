from django.db import models
from django.db.models import Q
from . import *
import mechanize
from BeautifulSoup import BeautifulSoup

class Cell(Product):    
    pricing = models.OneToOneField(CellPricing)
    phone = models.ForeignKey(Cellphone)
    best_price = models.IntegerField()
    
    def raw_text(self):
        return ''

    def __unicode__(self):
        return str(self.phone)
        
    def load_similar_products(self):
        pass
    
    @staticmethod
    def get_valid():
        return Cell.objects.filter(shp__isnull = False)
        
    @classmethod
    def custom_update(self):
        from solonotebooks.fetch_scripts import *
        for cell_company in CellCompany.objects.all():
            cell_company.cellpricingplan_set.all().delete()
            CellPricingTier.objects.filter(pricing__company = cell_company).delete()
            
            plans = cell_company.fetch_store.get_plans()
            for plan in plans:
                CellPricingPlan.new(plan, cell_company).save()
                
            cell_plans = cell_company.cellpricingplan_set.filter(price__gt = 0)
            
            for shpe in cell_company.store.storehasproductentity_set.filter(is_available = True, is_hidden = False):
                pricing, created = CellPricing.objects.get_or_create(url = shpe.url, company = cell_company)
                if created:
                    pricing.name = shpe.custom_name
                    pricing.save()
                cell_company.fetch_store.calculate_tiers(shpe, cell_plans, pricing)
                
        for cell in Cell.objects.all():
            tiers = CellPricingTier.objects.filter(pricing__cell = cell).filter(plan__price__gt = 0, cellphone_price__gt = 0).order_by('cellphone_price')
            if not tiers:
                tiers = CellPricingTier.objects.filter(pricing__cell = cell).filter(plan__price = 0).order_by('cellphone_price')
                
            if tiers:
                cell.best_price = tiers[0].cellphone_price
            else:
                cell.best_price = 0
            
            cell.save()
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
        
    
