#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import operator
import urllib
from datetime import datetime, date, timedelta
from time import time
from math import ceil
from django.db.models import Min, Max, Q
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

def manager_login_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_staff:
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
    
    name = 'Nuevas entidades'
    url = reverse('solonotebooks.cotizador.views_manager.new_entities')
    tabs.append([-1, name, url])
    
    name = u'Tiendas'
    url = reverse('solonotebooks.cotizador.views_manager.stores')
    tabs.append([-1, name, url])
    
    args['tabs'] = ['Administración', tabs]
    return append_metadata_to_response(request, template, args)

@manager_login_required    
def polymorphic_admin_request(request, product_id):
    product = Product.objects.get(pk = product_id)
    url = '/admin/cotizador/' + product.ptype.adminurlname + '/' + str(product.id)
    return HttpResponseRedirect(url)
    
@manager_login_required    
def clone_product(request, product_id):
    product = Product.objects.get(pk = product_id).get_polymorphic_instance()
    cloned_product = product.clone_product()
    
    url = reverse('solonotebooks.cotizador.views_manager.polymorphic_admin_request', args = [cloned_product.id])
    return HttpResponseRedirect(url)
    
@manager_login_required    
def news(request):
    # Shows the logs for the last week
    today = date.today()
    last_logs = LogEntry.objects.filter(date__gte = today - timedelta(days = 1)).order_by('-date').all()
    return append_manager_ptype_to_response(request, 'manager/news.html', {
            'last_logs': last_logs,
        })
        
@manager_login_required    
def new_entities(request):
    # Shows the models that don't have an associated product in the DB (i.e.: pending)
    new_entities = StoreHasProductEntity.objects.filter(is_hidden = False).filter(is_available = True).filter(shp__isnull = True)
    return append_manager_ptype_to_response(request, 'manager/new_entities.html', {
            'new_entities': new_entities,
        })
        
@manager_login_required
def storehasproductentity_edit(request, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)

    if request.method == 'POST':
        form = StoreHasProductEntityEditForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']

            if shpe.shp:
                shp = shpe.shp
                shpe.shp = None
                shpe.save()
                shp.update(recursive = True)
            
            shps = StoreHasProduct.objects.filter(product = product)
            created = True
            
            for sub_shp in shps:
                if sub_shp.store == shpe.store:
                    shp = sub_shp
                    created = False
                    break
                    
            if created:
                shp = StoreHasProduct()
                shp.product = product
                shp.save()

            shpe.shp = shp
            
            if not shpe.date_resolved:
                shpe.date_resolved = datetime.now()
                
            shpe.save()
                
            shp.update(recursive = True)
            return HttpResponseRedirect('/manager/new_entities/?refresh=true')
    else:
        d = {}
        
        store = shpe.infer_store()
        if store:
            d['store'] = store
            
        form = StoreHasProductEntityEditForm(d)
        
    if shpe.ptype:
        options = shpe.ptype.get_class().objects.all()
    else:
        options = Product.get_all_ordered()
        
    return append_manager_ptype_to_response(request, 'manager/store_has_product_entity_edit.html', {
        'shpe_form': form,
        'shpe': shpe,
        'options': options
    })
        
@manager_login_required
def storehasproductentity_hide(request, store_has_product_entity_id):
    # Makes a model invisible to the "pending" page if it is stupid (e.g. iPad)
    # or doesn't apply (combos of products + printers, accesories, etc)
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    shpe.is_hidden = True
    shpe.save()
    shpe.update(recursive = True)
    return HttpResponseRedirect('/manager/new_entities/?refresh=true');
    
@manager_login_required
def storehasproductentity_change_ptype(request, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    ptype = ProductType.objects.get(classname = request.GET['classname'])
    shpe.ptype = ptype
    shpe.save()
    url = reverse('solonotebooks.cotizador.views_manager.storehasproductentity_edit', args = [shpe.id])
    return HttpResponseRedirect(url);
    
@manager_login_required
def storehasproductentity_show(request, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    shpe.is_hidden = False
    shpe.save()
    shpe.update(recursive = True)
    url = reverse('solonotebooks.cotizador.views_manager.storehasproductentity_edit', args = [shpe.id])    
    return HttpResponseRedirect(url);
    
@manager_login_required
def storehasproductentity_refresh_price(request, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    shpe.update_price()
    shpe.save()
    url = reverse('solonotebooks.cotizador.views_manager.storehasproductentity_edit', args = [shpe.id])
    return HttpResponseRedirect(url)
    
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
def analyze_searches(request):
    import cairo
    from pycha.pie import PieChart

    results = {}
    sf = initialize_search_form(request.GET)
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
            

