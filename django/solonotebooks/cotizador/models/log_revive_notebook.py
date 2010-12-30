from datetime import date
from django.db import models
from utils import prettyPrice
from solonotebooks.cotizador.models import LogEntry, Notebook, NotebookSubscription

class LogReviveNotebook(models.Model):
    notebook = models.ForeignKey(Notebook)
    log_entry = models.ForeignKey(LogEntry)
    
    @staticmethod    
    def new(ntbk):
        log_revive_notebook = LogReviveNotebook()
        log_revive_notebook.notebook = ntbk
        log_revive_notebook.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_revive_notebook.save()
        return log_revive_notebook
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.notebook)
        
    def message(self):
        return str(self.notebook)  + ' (<a href="/notebooks/' + str(self.notebook.id) + '/">Link</a> / <a href="/admin/cotizador/notebook/' + str(self.notebook.id) + '/">Editar</a>)'
        
    def send_notification_mails(self):
            from solonotebooks.cotizador.models import MailReviveNotebook
        
            active_subscriptions = NotebookSubscription.objects.filter(notebook = self.notebook).filter(email_notifications = True).filter(user__is_active = True).filter(is_active = True)
            for subscription in active_subscriptions:
                MailReviveNotebook.new(subscription, self)        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log revive notebook'
