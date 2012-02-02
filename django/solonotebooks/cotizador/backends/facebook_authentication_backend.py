import json
import urllib
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.utils import send_facebook_registration_mail
from django.contrib.auth.models import User

class FacebookAuthenticationBackend:
    def authenticate(self, user_id, access_token):
        url = 'https://graph.facebook.com/%s?access_token=%s' % (user_id, access_token)
        user_data = json.load(urllib.urlopen(url))

        if 'error' in user_data:
            return None

        username = user_data['id']

        try:
            profile = UserProfile.objects.get(user__username = username)
            user = profile.user

            profile.facebook_name = user_data['name']
            profile.email = user_data['email']
            profile.save()

        except UserProfile.DoesNotExist:
            user = User.objects.create_user(username, user_data['email'])
            user.is_active = True
            user.save()

            profile = user.get_profile()
            profile.facebook_name = user_data['name']
            profile.save()

            send_facebook_registration_mail(user)

        return user
            
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None


