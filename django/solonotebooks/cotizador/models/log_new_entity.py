from datetime import date
from django.db import models
from . import LogEntry, StoreHasProductEntity

class LogNewEntity(models.Model):
    shpe = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry)
    
    @staticmethod
    def new(shpe):
        log_new_entity = LogNewEntity()
        log_new_entity.shpe = shpe
        log_new_entity.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        return log_new_entity
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.shpe)
        
    def message(self):
        return str(self.shpe) + ' (<a href="' + self.shpe.url + '">Link</a> / <a href="/admin/cotizador/storehasproductentity/' + str(self.shpe.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log new entity'
