#-*- coding: UTF-8 -*-
import hashlib
import cairo
import pycha.line
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
    
def send_email(user, subject, template, args):
    args['server_name'] = settings.SERVER_NAME
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [ user.username + '<' + user.email + '>' ])
    
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
    subject = 'Confirmación correo electrónico de SoloNotebooks'
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()
    
    t = get_template(template)
    args = {'user_digest': user_digest}
    
    send_email(user, subject, t, args)
    
def send_password_regeneration_mail(user):
    subject = 'Regeneración de contraseña de SoloNotebooks'
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.password).hexdigest()
    
    t = get_template('mails/password_regeneration_mail.html')
    args = {'user_digest': user_digest}
    send_email(user, subject, t, args)    
    
def send_new_password_mail(user, new_password):
    subject = 'Nueva contraseña de SoloNotebooks'
    
    t = get_template('mails/new_password_mail.html')
    args = {'new_password': new_password}
    
    send_email(user, subject, t, args)    
    
# Helper method to set the search_form for almost all of the views            
def initialize_search_form(data):
    qd = data.copy()
    search_form = NotebookSearchForm(qd)
    search_form.validate()
    search_form.is_valid()
    
    return search_form    
    
def generateChart(ntbk):
    npcs = NotebookPriceChange.objects.filter(notebook = ntbk).order_by('date')
    min_price = npcs.aggregate(Min('price'))['price__min']
    max_price = npcs.aggregate(Max('price'))['price__max'] 
    indexed_npcs = [[i, npcs[i]] for i in range(len(npcs))]
    
    last_npc = indexed_npcs[len(indexed_npcs) - 1][1]
    new_npc = deepcopy(last_npc)
    new_npc.date = date.today()
    indexed_npcs += [[len(indexed_npcs), new_npc]]

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 300)
    lines = [[inpc[0], inpc[1].price] for inpc in indexed_npcs]
        
    dataSet = (
        ('lines', [(k, v) for k, v in lines]),
        )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=inpc[0], label=str(inpc[1].date.day) + '/' + str(inpc[1].date.month)) for inpc in indexed_npcs],
            },
            'y': {
                'tickCount': 4,
                'range': (min_price / 1.3, max_price * 1.2)
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
            'hide': True,
        },
        'padding': {
            'left': 60,
            'bottom': 20,
            'right': 10,
        },
        'title': 'Cambios de precio a la fecha'
    }
    chart = pycha.line.LineChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + str(ntbk.id) + '.png')    
    
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
