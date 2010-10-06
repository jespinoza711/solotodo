from django.db import models
from django.contrib.auth.models import User
from solonotebooks.cotizador.models import Notebook

class NotebookSubscription(models.Model):
    notebook = models.ForeignKey(Notebook)
    user = models.ForeignKey(User)
    email_notifications = models.BooleanField()
    is_active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return self.user.username + ' - ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook subscription'
