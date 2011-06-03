from django.db import models
from django.db.models.signals import post_save  
from django.contrib.auth.models import User
from . import Store

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    confirmation_mails_sent = models.IntegerField(default = 0)
    change_mails_sent = models.IntegerField(default = 0)
    assigned_store = models.ForeignKey(Store, null = True, blank = True)
    facebook_name = models.CharField(max_length = 255, blank = True, null = True)
    can_access_competitivity_report = models.BooleanField(default=False)
    can_use_extra_ordering_options = models.BooleanField(default=False)

    def __str__(self):  
          return "%s's profile" % self.user  
          
    def name(self):
        if self.facebook_name:
            return self.facebook_name
        else:
            return self.user.username
            
    def allows_extra_ordering_options(self):
        return self.can_use_extra_ordering_options or self.user.is_superuser
            
    def can_access_services(self):
        return self.user.is_superuser or self.assigned_store != None
          
    class Meta:
        app_label = 'cotizador'

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user = instance)  

post_save.connect(create_user_profile, sender = User) 
