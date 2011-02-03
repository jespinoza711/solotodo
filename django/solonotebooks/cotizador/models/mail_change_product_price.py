from django.db import models
from django.template.loader import get_template
from . import ProductSubscription, LogChangeProductPrice
from solonotebooks import settings

class MailChangeProductPrice(models.Model):
    subscription = models.ForeignKey(ProductSubscription)
    log = models.ForeignKey(LogChangeProductPrice)
    success = models.BooleanField()
    
    @staticmethod
    def new(subscription, log):
        from solonotebooks.cotizador.utils import send_email
        
        m = MailChangeProductPrice()
        m.subscription = subscription
        m.log = log
        m.try_and_send_mail()
        
    def try_and_send_mail(self):
        try:
            t = get_template('mails/change_product_price.html')
            if not settings.DEBUG:
                send_email(self.subscription.user, 'Cambio de precio de ' + str(self.subscription.product), t, {'product': self.subscription.product })
            self.success = True
        except:
            self.success = False
        self.save()
    
    def __unicode__(self):
        return unicode(self.subscription) + ' - ' + unicode(self.log) 
    
    class Meta:
        app_label = 'cotizador'
