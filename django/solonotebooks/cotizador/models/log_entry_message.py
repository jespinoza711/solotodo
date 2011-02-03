from django.db import models
from . import LogEntry

class LogEntryMessage(models.Model):
    message = models.TextField()
    logEntry = models.ForeignKey(LogEntry)
    
    def __unicode__(self):
        return self.message
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log entry message'
