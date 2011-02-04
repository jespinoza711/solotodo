from datetime import date
from django.db import models
from utils import prettyPrice
from . import LogEntry, Product, ProductSubscription

class LogChangeProductPrice(models.Model):
    product = models.ForeignKey(Product)
    log_entry = models.ForeignKey(LogEntry) 
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    
    @staticmethod    
    def new(product, old_price, new_price):
        log_change_product_price = LogChangeProductPrice()
        log_change_product_price.product = product
        log_change_product_price.log_entry, created = LogEntry.objects.get_or_create(date = date.today())
        log_change_product_price.old_price = old_price
        log_change_product_price.new_price = new_price        
        log_change_product_price.save()
        return log_change_product_price
    
    
    def __unicode__(self):
        return str(self.log_entry.date) + ' - ' + str(self.product)
        
    def message(self):
        return str(self.product) + ' de ' + prettyPrice(self.old_price, '') + ' a ' + prettyPrice(self.new_price, '') + ' (<a href="/' + self.product.ptype.urlname + '/' + str(self.product.id) + '/">Link</a> / <a href="/admin/cotizador/' + self.product.ptype.adminurlname + '/' + str(self.product.id) + '/">Editar</a>)'
        
    def send_notification_mails(self):
        from . import MailChangeProductPrice
    
        active_subscriptions = ProductSubscription.objects.filter(product = self.product).filter(email_notifications = True).filter(user__is_active = True).filter(is_active = True)
        for subscription in active_subscriptions:
            MailChangeProductPrice.new(subscription, self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Log change product price'
