import urllib, hashlib
from django import template
from solonotebooks import settings

register = template.Library()

@register.inclusion_tag('templatetags/gravatar.html')
def show_gravatar(user, size = 48):
    default = settings.SERVER_NAME + 'media/assets/no-avatar.gif'

    email = ''
    if user and user.is_active:
        email = user.email

    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(), 
        'default': default, 
        'size': str(size)
    })

    return {'gravatar': {'url': url, 'size': size}}
    
    
