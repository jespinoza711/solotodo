from datetime import date
from django.db import models
from utils import prettyPrice
from solonotebooks.cotizador.models import LogEntry, Notebook, NotebookSubscription

class LogChangeNotebookPrice(models.Model):
    notebook = models.ForeignKey(Notebook)
    log_entry = models.ForeignKey(LogEntry) 
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    
    @staticmethod    
    def new(ntbk, old_price, new_price):
        log_change_notebook_price = LogChangeNotebookPrice()
        log_change_notebook_price.notebook = ntbk
        log_change_notebook_price.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_change_notebook_price.old_price = old_price
        log_change_notebook_price.new_price = new_price        
        log_change_notebook_price.save()
        return log_change_notebook_price
    
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.notebook)
        
    def message(self):
        return str(self.notebook) + ' de ' + prettyPrice(self.old_price, '') + ' a ' + prettyPrice(self.new_price, '') + ' (<a href="/notebooks/' + str(self.notebook.id) + '/">Link</a> / <a href="/admin/cotizador/notebook/' + str(self.notebook.id) + '/">Editar</a>)'
        
    def send_notification_mails(self):
        from solonotebooks.cotizador.models import MailChangeNotebookPrice
    
        active_subscriptions = NotebookSubscription.objects.filter(notebook = self.notebook).filter(email_notifications = True).filter(user__is_active = True)
        for subscription in active_subscriptions:
            MailChangeNotebookPrice.new(subscription, self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log change notebook price'
