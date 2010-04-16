from django.db import models

class LogEntry(models.Model):
    date = models.DateField()
    
    def __unicode__(self):
        return unicode(self.date)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log entry'
        verbose_name_plural = 'Log entries'
