from datetime import date
from django.db import models
from utils import prettyPrice
from . import LogEntry, StoreHasProductEntity

class LogChangeEntityName(models.Model):
    entity = models.ForeignKey(StoreHasProductEntity)
    log_entry = models.ForeignKey(LogEntry)
    old_name = models.CharField(max_length = 255)
    new_name = models.CharField(max_length = 255)
    
    @staticmethod    
    def new(entity, old_name, new_name):
        log = LogChangeEntityName()
        log.entity = entity
        log.old_name = old_name
        log.new_name = new_name
        log.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log.save()
        return log
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.entity)
        
    def message(self):
        message = str(self.entity.id) + ' de ' + str(self.old_name) + ' a ' + str(self.new_name)
        message += ' (<a href="/manager/storehasproductentity/' + str(self.entity.id) + '">Editar</a>'
        if self.entity.shp:
            message += ' / <a href="/products/' + str(self.entity.shp.product.id) + '">Link a producto</a>'
        message += ')'
        return message
        
    
    class Meta:
        app_label = 'cotizador'
        
