#-*- coding: UTF-8 -*-
from django.db import models
from django.template.loader import get_template
from solonotebooks.cotizador.models import NotebookSubscription, LogLostNotebook
from solonotebooks.cotizador.utils import send_email

class MailLostNotebook(models.Model):
    subscription = models.ForeignKey(NotebookSubscription)
    log = models.ForeignKey(LogLostNotebook)
    success = models.BooleanField()
    
    @staticmethod
    def new(subscription, log):
        m = MailLostNotebook()
        m.subscription = subscription
        m.log = log
        m.try_and_send_mail()
        
    def try_and_send_mail(self):
        try:
            t = get_template('mails/lost_notebook.html')
            send_email(self.subscription.user, str(self.subscription.notebook) + ' ya no está disponible', t, {'notebook': self.subscription.notebook })
            self.success = True
        except:
            self.success = False
        self.save()
    
    def __unicode__(self):
        return unicode(self.subscription) + ' - ' + unicode(self.log) 
    
    class Meta:
        app_label = 'cotizador'
