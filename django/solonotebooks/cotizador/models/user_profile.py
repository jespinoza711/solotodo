from django.db import models
from django.db.models.signals import post_save  
from django.contrib.auth.models import User
from solonotebooks.cotizador.models import Store

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    confirmation_mails_sent = models.IntegerField(default = 0)
    change_mails_sent = models.IntegerField(default = 0)
    assigned_store = models.ForeignKey(Store, null = True, blank = True)

    def __str__(self):  
          return "%s's profile" % self.user  
          
    class Meta:
        app_label = 'cotizador'

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user = instance)  

post_save.connect(create_user_profile, sender = User) 
