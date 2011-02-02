from datetime import date
from django.db import models
from solonotebooks.cotizador.models import LogEntry, StoreHasProductEntity

class LogLostModel(models.Model):
    shn = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry) 
    
    @staticmethod    
    def new(shn):
        log_lost_model = LogLostModel()
        log_lost_model.shn = shn
        log_lost_model.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        return log_lost_model
    
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.shn)
        
    def message(self):
        return str(self.shn) + ' (<a href="' + self.shn.url + '">Link</a> / <a href="/admin/cotizador/storehasproductentity/' + str(self.shn.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log lost model'
