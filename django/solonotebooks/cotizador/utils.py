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
    search_form = SearchForm(data)
    search_form.validate()
    search_form.is_valid()
    
    return search_form
    
def filter_notebooks(notebooks, search_form):
    if search_form.usage:
        value = search_form.usage
        if value == 1:
            notebooks = notebooks.filter(screen__size__family__base_size__gte = 13).filter(screen__size__family__base_size__lt = 16).filter(ram_quantity__value__gte = 2).filter(processor__speed_score__gte = 900).filter(storage_drive__capacity__value__gte = 160).distinct()
        elif value == 2:
            notebooks = notebooks.filter(screen__size__family__base_size__gte = 7).filter(screen__size__family__base_size__lt = 12).filter(Q(processor__line__family__id = 11)|Q(processor__line__family__id = 1))
        elif value == 3:
            notebooks = notebooks.filter(screen__size__family__base_size__gte = 11).filter(screen__size__family__base_size__lt = 13).filter(processor__line__family__id = 2)
        elif value == 4:
            notebooks = notebooks.filter(ram_quantity__value__gte = 2).filter(processor__speed_score__gte = 1300).filter(video_card__speed_score__gte = 3000).filter(storage_drive__capacity__value__gte = 250).distinct()
    
    if search_form.notebook_brand:
        notebooks = notebooks.filter(line__brand__id = search_form.notebook_brand)
        
    if search_form.processor_brand:
        notebooks = notebooks.filter(processor__line__family__brand__id = search_form.processor_brand)
        
    if search_form.processor_line_family:
        notebooks = notebooks.filter(processor__line__family__id = search_form.processor_line_family)
        
    if search_form.ram_quantity:
        notebooks = notebooks.filter(ram_quantity__value__gte = RamQuantity.objects.get(pk = search_form.ram_quantity).value)
        
    if search_form.storage_capacity:
        notebooks = notebooks.filter(storage_drive__capacity__value__gte = StorageDriveCapacity.objects.get(pk = search_form.storage_capacity).value).distinct()
        
    if search_form.screen_size_family:
        notebooks = notebooks.filter(screen__size__family__id = search_form.screen_size_family)
        
    if search_form.video_card_type:
        notebooks = notebooks.filter(video_card__card_type__id = search_form.video_card_type).distinct()
        
    if search_form.operating_system:
        notebooks = notebooks.filter(operating_system__family__id = search_form.operating_system)
        
    if search_form.notebook_line and search_form.advanced_controls:
        notebooks = notebooks.filter(line__id=search_form.notebook_line)
        
    if search_form.processor and search_form.advanced_controls:
        notebooks = notebooks.filter(processor__id=search_form.processor)
        
    if search_form.ram_type and search_form.advanced_controls:
        notebooks = notebooks.filter(ram_type__id=search_form.ram_type)
        
    if search_form.storage_type and search_form.advanced_controls:
        notebooks = notebooks.filter(storage_drive__drive_type__id = search_form.storage_type)
        
    if search_form.screen_resolution and search_form.advanced_controls:
        notebooks = notebooks.filter(screen__resolution__id = search_form.screen_resolution)
        
    if search_form.screen_touch and search_form.advanced_controls:
        notebooks = notebooks.filter(screen__is_touchscreen = search_form.screen_touch)    
        
    if search_form.video_card_brand and search_form.advanced_controls:
        notebooks = notebooks.filter(video_card__line__brand__id = search_form.video_card_brand).distinct()
        
    if search_form.video_card_line and search_form.advanced_controls:
        notebooks = notebooks.filter(video_card__line__id = search_form.video_card_line).distinct()
        
    if search_form.video_card and search_form.advanced_controls:
        notebooks = notebooks.filter(video_card__id = search_form.video_card).distinct()
        
    if search_form.min_price:
        notebooks = notebooks.filter(min_price__gte = int(search_form.min_price))

    if search_form.max_price:
        notebooks = notebooks.filter(min_price__lte = int(search_form.max_price))
        
    # Check the ordering orientation, if it is not set, each criteria uses 
    # sensible defaults (asc fro price, desc for cpu performance, etc)
    ordering_direction = [None, '', '-'][search_form.ordering_direction]
    
    # Apply the corresponding ordering based on the key
    if search_form.ordering == 1:
        if ordering_direction == None:
            ordering_direction = ''
        notebooks = notebooks.order_by(ordering_direction + 'min_price')
    elif search_form.ordering == 2:
        if ordering_direction == None:
            ordering_direction = '-'    
        notebooks = notebooks.order_by(ordering_direction + 'processor__speed_score')
    elif search_form.ordering == 3:
        if ordering_direction == None:
            ordering_direction = '-'    
        # Note: A notebook may have more than one video card, grab the fastest
        notebooks = notebooks.annotate(max_video_card_score=Max('video_card__speed_score')).order_by(ordering_direction + 'max_video_card_score')
    elif search_form.ordering == 4:
        if ordering_direction == None:
            ordering_direction = '-'    
        notebooks = notebooks.order_by(ordering_direction + 'ram_quantity__value')
    elif search_form.ordering == 5:
        if ordering_direction == None:
            ordering_direction = '-'    
        # Note: A notebook may have more than one SD, grab the biggest
        notebooks = notebooks.annotate(max_hard_drive_capacity=Max('storage_drive__capacity__value')).order_by(ordering_direction + 'max_hard_drive_capacity')        
    elif search_form.ordering == 6:
        if ordering_direction == None:
            ordering_direction = ''    
        notebooks = notebooks.order_by(ordering_direction + 'weight')
    else:
        if ordering_direction == None:
            ordering_direction = '-'    
        notebooks = notebooks.order_by(ordering_direction + 'date_added')    
        
    return [notebooks, ordering_direction]
    
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
                #'ticks': ['' for inpc in indexed_npcs],
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
        subscription = NotebookSubscription.objects.get(pk = subscription_id)
        if subscription.user != request.user or not subscription.is_active:
            raise SubscriptionException('Error de seguridad')
        subscription.email_notifications = new_mail_notification_status
        subscription.save()
    except SubscriptionException, e:
        request.flash['error'] = str(e)
    except Exception, e:
        request.flash['error'] = 'Error desconocido'
