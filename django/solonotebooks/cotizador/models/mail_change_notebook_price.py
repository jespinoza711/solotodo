from django.db import models
from django.template.loader import get_template
from solonotebooks.cotizador.models import NotebookSubscription, LogChangeNotebookPrice
from solonotebooks import settings

class MailChangeNotebookPrice(models.Model):
    subscription = models.ForeignKey(NotebookSubscription)
    log = models.ForeignKey(LogChangeNotebookPrice)
    success = models.BooleanField()
    
    @staticmethod
    def new(subscription, log):
        from solonotebooks.cotizador.utils import send_email
        
        m = MailChangeNotebookPrice()
        m.subscription = subscription
        m.log = log
        m.try_and_send_mail()
        
    def try_and_send_mail(self):
        try:
            t = get_template('mails/change_notebook_price.html')
            if not settings.DEBUG:
                send_email(self.subscription.user, 'Cambio de precio de ' + str(self.subscription.notebook), t, {'notebook': self.subscription.notebook })
            self.success = True
        except:
            self.success = False
        self.save()
    
    def __unicode__(self):
        return unicode(self.subscription) + ' - ' + unicode(self.log) 
    
    class Meta:
        app_label = 'cotizador'
