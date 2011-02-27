from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.utils import send_facebook_registration_mail
from django.contrib.auth.models import User

class FacebookAuthenticationBackend:
    def authenticate(self, username, email, facebook_name):
        try:
            profile = UserProfile.objects.get(user__username = username)
            return profile.user
        except:
            password = User.objects.make_random_password()
            
            user = User.objects.create_user(username, email, password)
            user.is_active = True
            user.save()
            profile = user.get_profile()
            profile.facebook_name = facebook_name
            profile.save()
            
            send_facebook_registration_mail(user)
            return user
            
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except:
            return None


