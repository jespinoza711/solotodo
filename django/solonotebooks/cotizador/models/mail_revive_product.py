#-*- coding: UTF-8 -*-
from django.db import models
from django.template.loader import get_template
from . import ProductSubscription, LogReviveProduct
from solonotebooks import settings

class MailReviveProduct(models.Model):
    subscription = models.ForeignKey(ProductSubscription)
    log = models.ForeignKey(LogReviveProduct)
    success = models.BooleanField()
    
    @staticmethod
    def new(subscription, log):
        m = MailReviveProduct()
        m.subscription = subscription
        m.log = log
        m.try_and_send_mail()
        
    def try_and_send_mail(self):
        from solonotebooks.cotizador.utils import send_email
        try:
            t = get_template('mails/revive_product.html')
            if not settings.DEBUG:
                send_email(self.subscription.user, str(self.subscription.product) + ' volvió a estar disponible', t, {'product': self.subscription.product })
            self.success = True
        except:
            self.success = False
        self.save()
    
    def __unicode__(self):
        return unicode(self.subscription) + ' - ' + unicode(self.log) 
    
    class Meta:
        app_label = 'cotizador'
