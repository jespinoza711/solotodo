from datetime import date
from django.db import models
from utils import prettyPrice
from . import LogEntry, Product, ProductSubscription

class LogLostProduct(models.Model):
    product = models.ForeignKey(Product)
    log_entry = models.ForeignKey(LogEntry)
    
    @staticmethod    
    def new(product):
        log_lost_product = LogLostProduct()
        log_lost_product.product = product
        log_lost_product.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_lost_product.save()
        return log_lost_product
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.product)
        
    def message(self):
        return str(self.product)
        
    def send_notification_mails(self):
            from . import MailLostProduct
        
            active_subscriptions = ProductSubscription.objects.filter(product = self.product).filter(email_notifications = True).filter(user__is_active = True).filter(is_active = True)
            for subscription in active_subscriptions:
                MailLostProduct.new(subscription, self)        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log lost product'
