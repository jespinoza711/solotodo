from datetime import date
from django.db import models
from solonotebooks.cotizador.models import LogEntry, Notebook

class LogLostNotebook(models.Model):
    notebook = models.ForeignKey(Notebook)
    log_entry = models.ForeignKey(LogEntry)
    
    @staticmethod    
    def new(ntbk):
        log_lost_notebook = LogLostNotebook()
        log_lost_notebook.notebook = ntbk
        log_lost_notebook.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        return log_lost_notebook
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.notebook)
        
    def message(self):
        return str(self.notebook) + ' (<a href="/admin/cotizador/notebook/' + str(self.notebook.id) + '/">Editar</a>)'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log lost notebook'
