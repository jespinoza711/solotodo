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
        result = ''
        result += ' ' + self.pricing.raw_text()
        result += ' ' + self.phone.raw_text()
        return result

    def __unicode__(self):
        result =  str(self.phone) + ' (' + str(self.pricing.company)
        if self.name.strip():
            result += ' / ' + self.name.strip()
        result += ')'
        return result
        
    def load_similar_products(self):
        pass
    
    @staticmethod
    def get_valid():
        return Cell.objects.filter(shp__isnull = False)
        
    def pretty_connectivity(self):
        result = []
        phone = self.phone
        
        if phone.has_bluetooth:
            result.append('Bluetooth')
        if phone.has_wifi:
            result.append('WiFi')
        if phone.has_3g:
            result.append('3G')
        if phone.has_gps:
            result.append('GPS')
            
        if result:
            return ' / '.join(result)
        else:
            return 'No posee'
            
    def extra_data(self, request):
        tiers = CellPricingTier.objects.filter(pricing__cell = self)
        result = {
            'phone': self.phone,
            'tiers': tiers,
        }
        
        if 'tier_id' in request.GET:
            result['tier_id'] = int(request.GET['tier_id'])
            
        return result
        
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
            cell.custom_local_update()
            cell.save()
            
    def custom_local_update(self):
        tiers = CellPricingTier.objects.filter(pricing__cell = self).filter(plan__price__gt = 0, cellphone_price__gt = 0).order_by('cellphone_price')
        if not tiers:
            tiers = CellPricingTier.objects.filter(pricing__cell = self).filter(plan__price = 0).order_by('cellphone_price')
            
        if tiers:
            self.best_price = tiers[0].cellphone_price
        else:
            self.best_price = 0
            
    def latest_price(self):
        if hasattr(self, 'is_sponsored'):
            return self.sponsored_shp.shpe.latest_price
        elif hasattr(self, 'price'):
            return self.price
        else:
            return self.best_price
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
        
    
