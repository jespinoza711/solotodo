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
from solonotebooks.cotizador.views import append_metadata_to_response
from models import *
from fields import *
from exceptions import *
from utils import *
from forms import *
import random

def services_user_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.flash['error'] = 'Por favor inicie sesión primero'
            return HttpResponseRedirect('/')
        elif not request.user.get_profile().assigned_store or not request.user.is_superuser:
            request.flash['error'] = 'Su cuenta no tiene permisos para acceder a esta sección'
            return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
@services_user_required
def product_details(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    form = DateRangeForm(request.GET)
    if not form.is_valid():
        form = DateRangeForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
    else:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        if end_date > date.today():
            end_date = date.today()
        if start_date >= end_date:
            url = reverse('solonotebooks.cotizador.views_services.product_details', args = [product.id])
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

    generate_timelapse_chart([chart_data], [u'Número de visitas'], 'services_product_' + str(product.id) + '_01.png', u'Número de visitas al producto en SoloTodo')
    
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
    
    generate_timelapse_chart(schart_data, ['Clicks totales a tiendas'], 'services_product_' + str(product.id) + '_02.png', u'Número de clicks a tiendas')
    
    # Third chart
    
    raw_data = ExternalVisit.objects.filter(shn__shp__product = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('shn__store').annotate(Count('id'))
    
    chart_data = [(unicode(Store.objects.get(pk = pair['shn__store'])), pair['id__count']) for pair in raw_data]
    store_distribution_data = chart_data
    
    generated_pie_chart = generate_pie_chart(chart_data, 'services_product_' + str(product.id) + '_03.png', u'Distribución de clicks entre tiendas')
    
    return append_metadata_to_response(request, 'services/product_details.html', {
        'product': product,
        'form': form,
        'tag': random.randint(1, 1000000),
        'product_prices': product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price'),
        'product_visit_count': product_visit_count,
        'all_external_visit_count': all_external_visit_count,
        'generated_pie_chart': generated_pie_chart,
        'store_distribution_data': store_distribution_data,
    })
    

