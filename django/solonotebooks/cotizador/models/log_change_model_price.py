from datetime import date
from django.db import models
from utils import prettyPrice
from solonotebooks.cotizador.models import LogEntry, StoreHasProductEntity

class LogChangeModelPrice(models.Model):
    shn = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry) 
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    
    @staticmethod    
    def new(shn, old_price, new_price):
        log_change_model_price = LogChangeModelPrice()
        log_change_model_price.shn = shn
        log_change_model_price.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_change_model_price.old_price = old_price
        log_change_model_price.new_price = new_price        
        return log_change_model_price
    
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.shn)
        
    def message(self):
        return str(self.shn) + ' de ' + prettyPrice(self.old_price, '') + ' a ' + prettyPrice(self.new_price, '') + ' (<a href="' + self.shn.url + '">Link</a> / <a href="/admin/cotizador/storehasproductentity/' + str(self.shn.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log change model price'
