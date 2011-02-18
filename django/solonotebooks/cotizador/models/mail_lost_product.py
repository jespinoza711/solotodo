#-*- coding: UTF-8 -*-
from django.db import models
from django.template.loader import get_template
from . import ProductSubscription, LogLostProduct
from solonotebooks import settings

class MailLostProduct(models.Model):
    subscription = models.ForeignKey(ProductSubscription)
    log = models.ForeignKey(LogLostProduct)
    success = models.BooleanField()
    
    @staticmethod
    def new(subscription, log):
        m = MailLostProduct()
        m.subscription = subscription
        m.log = log
        m.try_and_send_mail()
        
    def try_and_send_mail(self):
        from solonotebooks.cotizador.utils import send_email
        try:
            t = get_template('mails/lost_product.html')
            if not settings.DEBUG:
                send_email(self.subscription.user, str(self.subscription.product) + ' ya no está disponible', t, {'product': self.subscription.product })
            self.success = True
        except Exception, e:
            self.success = False
        self.save()
    
    def __unicode__(self):
        return unicode(self.subscription) + ' - ' + unicode(self.log) 
    
    class Meta:
        app_label = 'cotizador'
