from datetime import date
from django.db import models
from utils import prettyPrice
from . import LogEntry, Store

class LogFetchStoreError(models.Model):
    store = models.ForeignKey(Store)
    log_entry = models.ForeignKey(LogEntry)
    message = models.CharField(max_length = 255)
    
    @staticmethod    
    def new(store, message):
        log = LogFetchStoreError()
        log.store = store
        log.message = message
        log.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log.save()
        return log
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.store)
        
    def print_message(self):
        return str(self.store) + ': ' + str(self.message)
    
    class Meta:
        app_label = 'cotizador'
