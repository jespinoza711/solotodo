from datetime import date
from django.db import models
from utils import prettyPrice
from . import LogEntry, StoreHasProductEntity

class LogChangeEntityPrice(models.Model):
    shpe = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry) 
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    
    @staticmethod    
    def new(shpe, old_price, new_price):
        log_change_entity_price = LogChangeEntityPrice()
        log_change_entity_price.shpe = shpe
        log_change_entity_price.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_change_entity_price.old_price = old_price
        log_change_entity_price.new_price = new_price        
        return log_change_entity_price
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.shpe)
        
    def message(self):
        return str(self.shpe) + ' de ' + prettyPrice(self.old_price, '') + ' a ' + prettyPrice(self.new_price, '') + ' (<a href="' + self.shpe.url + '">Link</a> / <a href="/admin/cotizador/storehasproductentity/' + str(self.shpe.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log change entity price'
