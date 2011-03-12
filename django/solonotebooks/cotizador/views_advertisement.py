#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import operator
import urllib
from datetime import date, timedelta
from time import time
from math import ceil
from django.db.models import Min, Max, Q, Avg, Count
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlquote
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import email_re
from solonotebooks import settings
from solonotebooks.cotizador.views import append_ads_to_response
from models import *
from fields import *
from exceptions import *
from utils import *
from forms import *

def append_advertisement_ptype_to_response(request, template, args):
    args['ptypes'] = ProductType.objects.all()
    return append_ads_to_response(request, template, args)

def store_user_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.get_profile().assigned_store:
            request.flash['error'] = 'Por favor inicie sesión primero'
            return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
@store_user_required
def index(request):
    store = request.user.get_profile().assigned_store
    shpes = StoreHasProductEntity.objects.filter(store = store, is_available = True)
    
    non_indexable_shpes = shpes.filter(is_hidden = True)
    shpes = shpes.filter(is_hidden = False)
    
    non_indexed_shpes = shpes.filter(shp__isnull = True)
    shpes = shpes.filter(shp__isnull = False)
    
    product_pairs = list(set([(shpe.shp, shpe.shp.product) for shpe in shpes if shpe.shp.product.ptype.classname == 'Notebook']))
    product_pairs = sorted(product_pairs, key = lambda pair: unicode(pair[1]))
    
    unavailable_products = []
    reserved_products = []
    free_products = []
    
    for product_pair in product_pairs:
        product = product_pair[1]
        if not product.sponsored_shp:
            free_products.append(product_pair)
        elif product.sponsored_shp.shpe.store == store:
            reserved_products.append(product_pair)
        else:
            unavailable_products.append(product_pair)            
    
    return append_advertisement_ptype_to_response(request, 'advertisement/index.html', {
        'store': store,
        'non_indexable_shpes': non_indexable_shpes,
        'non_indexed_shpes': non_indexed_shpes,
        'unavailable_products': unavailable_products,
        'reserved_products': reserved_products,
        'free_products': free_products
    })
    
    
@store_user_required
def reserve_slots(request):
    store = request.user.get_profile().assigned_store
    shp_ids = request.POST.getlist('selected_products[]')
    shps = [StoreHasProduct.objects.get(pk = shp_id) for shp_id in shp_ids]
    for shp in shps:
        if shp.shpe.store != store:
            raise Exception
        if shp.product.sponsored_shp:
            raise Exception
    reserved_shps_count = Product.objects.filter(sponsored_shp__shpe__store = store).count()
    if len(shps) + reserved_shps_count > store.sponsor_cap:
        request.flash['error'] = 'Limite de anuncios excedido'
        return HttpResponseRedirect('/advertisement?refresh=true')
    for shp in shps:
        shp.product.sponsored_shp = shp
        shp.product.save()
    request.flash['message'] = 'Suscripciones agregadas'
    return HttpResponseRedirect('/advertisement?refresh=true')
    
@store_user_required
def free_slots(request):
    store = request.user.get_profile().assigned_store
    shp_ids = request.POST.getlist('selected_products[]')
    shps = [StoreHasProduct.objects.get(pk = shp_id) for shp_id in shp_ids]
    for shp in shps:
        if not shp.product.sponsored_shp:
            raise Exception
        if shp.product.sponsored_shp.shpe.store != store:
            raise Exception
    for shp in shps:
        shp.product.sponsored_shp = None
        shp.product.save()
    request.flash['message'] = 'Suscripciones liberadas'
    return HttpResponseRedirect('/advertisement?refresh=true')
    
@store_user_required
def slot_details(request, shp_id):
    store = request.user.get_profile().assigned_store
    shp = StoreHasProduct.objects.get(pk = shp_id)
    product = shp.product
    if shp.shpe.store != store:
        raise Exception
    
    form = AdvertisementSlotDetailsForm(request.GET)
    if not form.is_valid():
        form = AdvertisementSlotDetailsForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
        end_string = '#'
    else:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        if end_date > date.today():
            end_date = date.today()
        if start_date >= end_date:
            url = reverse('solonotebooks.cotizador.views_advertisement.slot_details', args = [shp.id])
            return HttpResponseRedirect(url)
        
    # First chart
    
    raw_data = ProductVisit.objects.filter(notebook = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).extra(select = {'d': 'CAST(date AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = dict([(entry['d'], entry['id__count']) for entry in raw_data])
    
    sdate = start_date
    step_date = timedelta(days = 1)
    
    while sdate <= end_date:
        if sdate not in chart_data:
            chart_data[sdate] = 0
        sdate += step_date
    
    chart_data = chart_data.items()
    chart_data = sorted(chart_data, key = lambda pair: pair[0])
    
    product_visit_count = sum([e[1] for e in chart_data])

    generate_timelapse_chart([chart_data], [u'Número de visitas'], 'unit_' + str(shp.id) + '_01.png', u'Número de visitas al producto en SoloTodo')
    
    # Second chart
    
    raw_data = ExternalVisit.objects.filter(shn__shp__product = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('date').annotate(Count('id')).order_by('date')
    chart_data = dict([(entry['date'], entry['id__count']) for entry in raw_data])
    
    sdate = start_date
    step_date = timedelta(days = 1)
    
    while sdate <= end_date:
        if sdate not in chart_data:
            chart_data[sdate] = 0
        sdate += step_date
    
    chart_data = chart_data.items()
    chart_data = sorted(chart_data, key = lambda pair: pair[0])
    
    all_external_visit_count = sum([e[1] for e in chart_data])
    
    schart_data = [chart_data]
    
    raw_data = ExternalVisit.objects.filter(shn__shp__product = product, shn__store = store, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('date').annotate(Count('id')).order_by('date')
    chart_data = dict([(entry['date'], entry['id__count']) for entry in raw_data])
    
    sdate = start_date
    step_date = timedelta(days = 1)
    
    while sdate <= end_date:
        if sdate not in chart_data:
            chart_data[sdate] = 0
        sdate += step_date
    
    chart_data = chart_data.items()
    chart_data = sorted(chart_data, key = lambda pair: pair[0])

    store_external_visit_count = sum([e[1] for e in chart_data])

    schart_data.append(chart_data)
    generate_timelapse_chart(schart_data, ['Clicks totales', 'Clicks a ' + unicode(store)], 'unit_' + str(shp.id) + '_02.png', u'Número de clicks a tiendas')
    
    # Third chart
    
    raw_data = ExternalVisit.objects.filter(shn__shp__product = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('shn__store').annotate(Count('id'))
    chart_data = [(unicode(Store.objects.get(pk = pair['shn__store'])), pair['id__count']) for pair in raw_data]
    
    generate_pie_chart(chart_data, 'unit_' + str(shp.id) + '_03.png', u'Distribución de clicks entre tiendas')
        
    return append_advertisement_ptype_to_response(request, 'advertisement/slot_details.html', {
        'store': store,
        'shp': shp,
        'product': shp.product,
        'form': form,
        'tag': datetime.now().toordinal(),
        'product_prices': product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price'),
        'product_visit_count': product_visit_count,
        'store_external_visit_count': store_external_visit_count,
        'all_external_visit_count': all_external_visit_count
    })
