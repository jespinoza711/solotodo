from datetime import date
from django.db import models
from . import LogEntry, StoreHasProductEntity

class LogReviveEntity(models.Model):
    shpe = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry)
    
    @staticmethod    
    def new(shpe):
        log_revive_entity = LogReviveEntity()
        log_revive_entity.shpe = shpe
        log_revive_entity.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        return log_revive_entity
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.shpe)
        
    def message(self):
        return str(self.shpe)  + ' (<a href="' + self.shpe.url + '">Link</a> / <a href="/admin/cotizador/storehasproductentity/' + str(self.shpe.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log revive entity'
