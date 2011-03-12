#-*- coding: UTF-8 -*-
import hashlib
from copy import deepcopy
from random import randint
from datetime import date, datetime
from django.db.models import Min, Max
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from solonotebooks import settings
from models import *
from forms import *
from exceptions import *

def stringCompare(comp1, comp2):
    comp1_words = comp1.lower().split()
    comp2_words = comp2.lower().split()
    counter = 0;
    for word in comp2_words:
        for comp1_word in comp1_words:
            if word in comp1_word:
                counter += 1;
                break
            
    return 100.0 * counter / len(comp2_words)

def load_advertisement(position):
    try:
        ads = Advertisement.objects.filter(position__name = position).filter(is_active = True)
        ad_index = randint(0, len(ads) - 1)
        ad = ads[ad_index]
        ad.impressions += 1
        ad.save()
    except:
        ad = None
        
    return ad
    
def send_email(user, subject, template, args = {}):
    args['server_name'] = settings.SERVER_NAME
    args['site_name'] = settings.SITE_NAME
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [ user.username + '<' + user.email + '>' ])
    
def send_facebook_registration_mail(user):
    subject = 'Registro en ' + settings.SITE_NAME
    t = get_template('mails/facebook_registration_mail.html')
    
    send_email(user, subject, t)
    
def send_signup_mail(user):
    if user.get_profile().confirmation_mails_sent >= 5:
        raise MailException('Superado el límite de correos de confirmación que se pueden enviar')
    else:
        send_confirmation_mail_from_template(user, 'mails/confirmation_mail.html')
        user.get_profile().confirmation_mails_sent += 1
        user.get_profile().save()
        
def send_change_mail(user):
    if user.get_profile().change_mails_sent >= 5:
        raise MailException('Superado el límite de solicitud de cambios de correo')
    else:
        send_confirmation_mail_from_template(user, 'mails/change_email.html')
        user.get_profile().change_mails_sent += 1
        user.get_profile().save()        
    
def send_confirmation_mail_from_template(user, template):
    subject = 'Confirmación correo electrónico de ' + settings.SITE_NAME
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()
    
    t = get_template(template)
    args = {'user_digest': user_digest}
    
    send_email(user, subject, t, args)
    
def send_password_regeneration_mail(user):
    subject = 'Regeneración de contraseña de ' + settings.SITE_NAME
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.password).hexdigest()
    
    t = get_template('mails/password_regeneration_mail.html')
    args = {'user_digest': user_digest}
    send_email(user, subject, t, args)    
    
def send_new_password_mail(user, new_password):
    subject = 'Nueva contraseña de ' + settings.SITE_NAME
    
    t = get_template('mails/new_password_mail.html')
    args = {'new_password': new_password}
    
    send_email(user, subject, t, args)    
    
# Helper method to set the search_form for almost all of the views            
def initialize_search_form(data, ptype = ProductType.default()):
    if not ptype:
        return None
    qd = data.copy()
    search_form_class = eval(ptype.classname + 'SearchForm')
    search_form = search_form_class(qd)
    search_form.validate()
    search_form.is_valid()
    
    return search_form
    
def set_subscription_mail_notifications(request, subscription_id, new_mail_notification_status):
    try:
        subscription = ProductSubscription.objects.get(pk = subscription_id)
        if subscription.user != request.user or not subscription.is_active:
            raise SubscriptionException('Error de seguridad')
        subscription.email_notifications = new_mail_notification_status
        subscription.save()
    except SubscriptionException, e:
        request.flash['error'] = str(e)
    except Exception, e:
        request.flash['error'] = 'Error desconocido'
        
def concat_dictionary(d):
    vals = ['%s=%s' % (k, v) for k, v in d.items()]
    if vals:
        return '?' + '&'.join(vals)
    else:
        return ''
        
def generate_timelapse_chart(data_streams, legends, filename, title):
    import cairo
    import pycha.line
    from copy import deepcopy
    
    main_data_stream = data_streams[0]
    
    values = [v for k, v in main_data_stream]
    
    maxi = max(values)
    r = (main_data_stream[0][0].toordinal(), main_data_stream[-1][0].toordinal())
    
    chart_data_set = [(legends[idx], [(k.toordinal(), v) for k, v in l]) for idx, l in enumerate(data_streams)]
        
    dataSet = chart_data_set

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v = k.toordinal(), label = str(k.day) + '/' + str(k.month)) for k, v in main_data_stream],
                'range': r
            },
            'y': {
                'tickCount': 4,
                'range': (0, maxi * 1.2)
            }
        },
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444',
            'baseColor': '#FFFFFF',
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'blue',
            },
        },
        'legend': {
            #'hide': True,
        },
        'padding': {
            'left': 60,
            'bottom': 20,
            'right': 10,
        },
        'title': title
    }
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 850, 400)
    chart = pycha.line.LineChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + filename)
    
def generate_pie_chart(data, filename, title):
    import cairo
    import pycha.pie
    from copy import deepcopy
        
    dataSet = [(entry[0], [[0, entry[1]]]) for entry in data]

    options = {
        'axis': {
            'x': {
                #'ticks': [dict(v = k.toordinal(), label = str(k.day) + '/' + str(k.month)) for k, v in main_data_stream],
                #'range': r
            },
            'y': {
                'tickCount': 4,
                #'range': (0, maxi * 1.2)
            }
        },
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444',
            'baseColor': '#FFFFFF',
        },
        'colorScheme': {
            'name': 'rainbow', 
            'args': 
                {'initialColor': 'red'}
        },
        'legend': {
            #'hide': True,
        },
        'padding': {
            #'left': 60,
            #'bottom': 20,
            #'right': 10,
        },
        'title': title
    }
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 890, 500)
    chart = pycha.pie.PieChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + filename)
    
