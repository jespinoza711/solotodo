#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import operator
import urllib
from datetime import datetime, date, timedelta
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
from models import *
from fields import *
from exceptions import *
from utils import *
from views import *
from views_store import _registry, _advertisement, _statistics
from forms import *
import random

def manager_login_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/account/login')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
def append_manager_ptype_to_response(request, template, args):
    tabs = []
    
    name = 'Noticias'
    url = reverse('solonotebooks.cotizador.views_manager.news')
    tabs.append([-1, name, url])
    
    name = u'Tiendas'
    url = reverse('solonotebooks.cotizador.views_manager.stores')
    tabs.append([-1, name, url])
    
    name = u'Staff'
    url = reverse('solonotebooks.cotizador.views_manager.staff')
    tabs.append([-1, name, url])
    
    name = u'Estadísticas'
    url = reverse('solonotebooks.cotizador.views_manager.statistics')
    tabs.append([-1, name, url])
    
    args['tabs'] = ['Administración', tabs]
    return append_metadata_to_response(request, template, args)
    
@manager_login_required
def statistics(request):
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
            url = reverse('solonotebooks.cotizador.views_manager.statistics')
            return HttpResponseRedirect(url)
    
    # First chart: Number of SHPEs appereances per day

    raw_data = StoreHasProductEntity.objects.filter(date_added__gte = start_date, date_added__lt = end_date + timedelta(days = 1)).extra(select = {'d': 'CAST(date_added AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de nuevas entidades'], 'manager_statistics_01.png', u'Número de nuevas entidades registradas')
    
    shpes_created_count = sum([e[1] for e in chart_data])
    
    # Second chart: Number of SHPEs resolved per day

    raw_data = StoreHasProductEntity.objects.filter(date_added__gte = start_date, date_added__lt = end_date + timedelta(days = 1), date_resolved__isnull = False).extra(select = {'d': 'CAST(date_resolved AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de entidades asociadas'], 'manager_statistics_02.png', u'Número de entidades asociadas')
    
    shpes_associated_count = sum([e[1] for e in chart_data])
    
    # Third chart: Number of products created per day

    raw_data = Product.objects.filter(date_added__gte = start_date, date_added__lt = end_date + timedelta(days = 1)).extra(select = {'d': 'CAST(date_added AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de productos creados'], 'manager_statistics_03.png', u'Número de productos creados')
    
    product_creation_count = sum([e[1] for e in chart_data])
    
    return append_manager_ptype_to_response(request, 'manager/statistics.html', {
            'form': form,
            'shpes_created_count': shpes_created_count,
            'shpes_associated_count': shpes_associated_count,
            'product_creation_count': product_creation_count,
            'tag': random.randint(1, 1000000),
        })
    
@manager_login_required    
def news(request):
    # Shows the logs for the last week
    today = date.today()
    last_logs = LogEntry.objects.filter(date__gte = today - timedelta(days = 1)).order_by('-date').all()
    return append_manager_ptype_to_response(request, 'manager/news.html', {
            'last_logs': last_logs,
        })
    
@manager_login_required
def stores(request):
    stores = Store.objects.all()
    return append_manager_ptype_to_response(request, 'manager/stores.html', {
            'stores': stores,
        })
        
@manager_login_required
def store_details(request, store_id):
    store = Store.objects.get(pk = store_id)
    args =  _registry(request, store)
    if 'url' in args:
        return HttpResponseRedirect(args['url'])
    else:
        return append_manager_ptype_to_response(request, 'manager/store_details.html', args)
    
@manager_login_required
def store_advertisement(request, store_id):
    store = Store.objects.get(pk = store_id)
    args =  _advertisement(store)
    return append_manager_ptype_to_response(request, 'manager/store_advertisement.html', args)
    
@manager_login_required
def store_statistics(request, store_id):
    store = Store.objects.get(pk = store_id)
    args =  _statistics(request, store)
    return append_manager_ptype_to_response(request, 'manager/store_statistics.html', args)

@manager_login_required
def staff(request):
    staff = User.objects.filter(is_staff=True, is_superuser=False)
    args = {'staff': staff}
    return append_manager_ptype_to_response(request, 'manager/staff.html', args)
    
@manager_login_required            
def analyze_searches(request):
    import cairo
    from pycha.pie import PieChart

    results = {}
    sf = initialize_search_form(request)
    for field_name, field in sf.fields.items():
        if isinstance(field, ClassChoiceField) or isinstance(field, CustomChoiceField):
            results[field] = {'data': {}, 'meta': {'total': 0}}
        
    srs = SearchRegistry.objects.filter(date__gte = date.today() - timedelta(days = 7)) 
    num_queries = len(srs)
    
    folder = settings.MEDIA_ROOT + '/temp/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass
    
    for sr in srs:
        key_vals = sr.query.split('&')
        for key_val in key_vals:
            vals = key_val.split('=')
            field_name = vals[0]
            field = sf.fields[field_name]
            if not (isinstance(field, ClassChoiceField) or isinstance(field, CustomChoiceField)):
                continue
                
            val = vals[1]
            str_val = field.get_object_name(val)
            if str_val not in results[field]['data']:
                results[field]['data'][str_val] = [0, 0]
            results[field]['data'][str_val][0] += 1
            results[field]['meta']['total'] += 1
            
    for field, field_dict in results.items():
        try: 
            results[field]['meta']['percentage'] = 100.0 * results[field]['meta']['total'] / num_queries
        except:
            results[field]['meta']['percentage'] = 0.0
        sub_total = results[field]['meta']['total']
        for field_option, sub_results in field_dict['data'].items():
            sub_results[1] = 100.0 * sub_results[0] / sub_total
            
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 400)
        chart = PieChart(surface)
                
        dataSet = [(field_option, [[0, sub_results[1]]]) for field_option, sub_results in field_dict['data'].items()]
        if dataSet:
            chart.addDataset(dataSet)
            chart.render()
            filename = folder + str(field.name) + "-" + str(num_queries) + ".png"
            surface.write_to_png(filename)
            results[field]['meta']['is_available'] = True
        else:
            results[field]['meta']['is_available'] = False
            
    return append_manager_ptype_to_response(request, 'manager/analyze_searches.html', {
                'form': sf,
                'results': results,
                'num_queries': num_queries,
            })
