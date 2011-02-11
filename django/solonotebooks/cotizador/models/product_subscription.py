from django.db import models
from django.contrib.auth.models import User
from . import Product

class ProductSubscription(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    email_notifications = models.BooleanField()
    is_active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return self.user.username + ' - ' + unicode(self.product)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product subscription'
