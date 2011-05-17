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
import xlwt
from xlwt import Workbook, easyxf, Formula
import random

def append_store_metadata_to_response(request, template, args):
    tabs = [
            u'Opciones de admistración', 
            [
                    ['Registro', reverse('solonotebooks.cotizador.views_store.registry')],
                    ['Estadísticas', reverse('solonotebooks.cotizador.views_store.statistics')]
            ]
        ]
        
    if request.user.get_profile().can_access_competitivity_report:
        tabs[1].append(['Informe de competitividad', reverse('solonotebooks.cotizador.views_store.competition_report')],)
        
    args['tabs'] = tabs
    return append_metadata_to_response(request, template, args)

def store_user_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated() or (not request.user.get_profile().assigned_store and not request.user.is_superuser):
            request.flash['error'] = 'Por favor inicie sesión primero'
            return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
@store_user_required
def competition_report(request):
    try:
        form, store, results = _competition_data(request)
    except:
        request.flash['error'] = 'Usted no tiene permisos para acceder a esta sección'
        return HttpResponseRedirect(reverse('solonotebooks.cotizador.views_store.registry'))
    
    return append_store_metadata_to_response(request, 'store/competitivity_report.html', {
        'form': form,
        'store': store,
        'results': results,
    })
    
def _competition_data(request):
    if not request.user.get_profile().can_access_competitivity_report:
        raise Exception

    form = CompetitivityReportOrdering(request.GET)
    if form.is_valid():
        ordering = form.cleaned_data['ordering']
    else:
        ordering = 1
    
    store = request.user.get_profile().assigned_store
    ptypes = ProductType.objects.all()
    results = []
    for ptype in ptypes:
        results.append([ptype.displayname, store.get_products_in_category(ptype, ordering)])
        
    return [form, store, results]

@store_user_required    
def index(request):
    return HttpResponseRedirect(reverse('solonotebooks.cotizador.views_store.registry'))
    
@store_user_required    
def registry(request):
    store = request.user.get_profile().assigned_store
    args =  _registry(request, store)
    if 'url' in args:
        return HttpResponseRedirect(args['url'])
    else:
        return append_store_metadata_to_response(request, 'store/registry.html', args)
    
    
def _registry(request, store):
    form = SearchShpeForm(request.GET)
    error_message = ''
    if request.GET and form.is_valid():
        url = form.cleaned_data['url']
        
        try:
            shpe = StoreHasProductEntity.objects.get(url = url)
        except StoreHasProductEntity.DoesNotExist, e:
            shpe = store.fetch_product_data(url)
        
        if shpe:
            follow_url = reverse('solonotebooks.cotizador.views_store.entity_details', args = [shpe.id])
            return { 'url': follow_url }
        else:
            error_message = u'El producto de la URL ingresada no está en nuestro índice, si cree que debiera estarlo por favor contáctenos.'
    else:    
        form = SearchShpeForm()
        
    try:
        filename = settings.LOG_DIRECTORY + store.classname + '_fetch.txt'
        f = open(filename)
        result_text = ''
        for line in f.readlines():
            result_text += line
    except Exception, e :
        result_text = 'No hay información de la última indexación de ' + str(store)
        
    pending_shpes = store.storehasproductentity_set.filter(shp__isnull = True, is_available = True, is_hidden = False)
    non_idx_shpes = store.storehasproductentity_set.filter(is_hidden = True, is_available = True)
    idx_shpes = store.storehasproductentity_set.filter(shp__isnull = False, is_available = True, is_hidden = False)
            
    return {
        'store': store,
        'result_text': result_text,
        'form': form,
        'error_message': error_message,
        'pending_shpes': pending_shpes,
        'non_idx_shpes': non_idx_shpes,
        'idx_shpes': idx_shpes,
    }
    
@store_user_required
def advertisement(request):
    store = request.user.get_profile().assigned_store
    args = _advertisement(store)           
    
    return append_store_metadata_to_response(request, 'store/advertisement.html', args)
    
def _advertisement(store):
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
    
    return {
        'store': store,
        'non_indexable_shpes': non_indexable_shpes,
        'non_indexed_shpes': non_indexed_shpes,
        'unavailable_products': unavailable_products,
        'reserved_products': reserved_products,
        'free_products': free_products
    }
    
@store_user_required
def statistics(request):
    store = request.user.get_profile().assigned_store
    args = _statistics(request, store)           
    
    return append_store_metadata_to_response(request, 'store/statistics.html', args)
    
def _statistics(request, store):
    form = DateRangeForm(request.GET)
    if not form.is_valid():
        form = DateRangeForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
        end_string = '#'
    else:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        if end_date > date.today():
            end_date = date.today()
        if start_date >= end_date:
            url = reverse('solonotebooks.cotizador.views_store.statistics')
            return HttpResponseRedirect(url)
           
    # Normal clicks 
    
    raw_data = ExternalVisit.objects.filter(shn__store = store, date__gte = start_date, date__lte = end_date).values('date').annotate(Count('id')).order_by('date')
    chart_data = [(entry['date'], entry['id__count']) for entry in raw_data]
    click_count = sum([e[1] for e in chart_data])

    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de visitas'], 'store_' + str(store.id) + '_01.png', u'Número de clicks normales a ' + str(store))
    
    # Sponsored clicks
    
    raw_data = SponsoredVisit.objects.filter(shp__shpe__store = store, date__gte = start_date, date__lte = end_date).values('date').annotate(Count('id')).order_by('date')
    chart_data = [(entry['date'], entry['id__count']) for entry in raw_data]
    
    sponsored_click_count = sum([e[1] for e in chart_data])

    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de visitas'], 'store_' + str(store.id) + '_02.png', u'Número de clicks patrocinados a ' + str(store))
    
    return {
        'store': store,
        'form': form,
        'click_count': click_count,
        'sponsored_click_count': sponsored_click_count,
        'tag': random.randint(1, 1000000)
        }
    
@store_user_required
def reserve_slots(request):
    store = request.user.get_profile().assigned_store
    referrer = request.META.get('HTTP_REFERER')
    shp_ids = request.POST.getlist('selected_products[]')
    shps = [StoreHasProduct.objects.get(pk = shp_id) for shp_id in shp_ids]
    for shp in shps:
        if shp.shpe.store != store and not request.user.is_superuser:
            raise Exception
        if shp.product.sponsored_shp:
            raise Exception
    reserved_shps_count = Product.objects.filter(sponsored_shp__shpe__store = store).count()
    if len(shps) + reserved_shps_count > store.sponsor_cap:
        request.flash['error'] = 'Limite de anuncios excedido'
        return HttpResponseRedirect(referrer)
    for shp in shps:
        shp.product.sponsored_shp = shp
        shp.product.save()
    request.flash['message'] = 'Suscripciones agregadas'
    return HttpResponseRedirect(referrer)
    
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
    referrer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referrer)
    
@store_user_required
def entity_details(request, shpe_id):
    store = request.user.get_profile().assigned_store
    shpe = StoreHasProductEntity.objects.get(pk = shpe_id)
    
    if shpe.store != store and not request.user.is_superuser:
        url = reverse('solonotebooks.cotizador.views_store.index')
        return HttpResponseRedirect(url)
    
    if shpe.is_hidden or not shpe.shp:
        return append_store_metadata_to_response(request, 'store/entity_details_no_data.html', {
            'store': store,
            'shpe': shpe,
        })
        
    shp = StoreHasProduct.objects.get(pk = shpe.shp.id)
    
    other_shpes = shp.storehasproductentity_set.filter(is_available = True).order_by('latest_price')
    if other_shpes.count() == 1:
        other_shpes = None
    
    
    product = shp.product
    
    form = DateRangeForm(request.GET)
    if not form.is_valid():
        form = DateRangeForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
        end_string = '#'
    else:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        if end_date > date.today():
            end_date = date.today()
        if start_date >= end_date:
            url = reverse('solonotebooks.cotizador.views_store.slot_details', args = [shp.id])
            return HttpResponseRedirect(url)
    
    if store.sponsor_cap:    
        # First chart
        
        raw_data = ProductVisit.objects.filter(notebook = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).extra(select = {'d': 'CAST(date AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
        chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
        
        product_visit_count = sum([e[1] for e in chart_data])

        generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de visitas'], 'unit_' + str(shp.id) + '_01.png', u'Número de visitas al producto en SoloTodo')
        
        # Second chart
        
        raw_data = ExternalVisit.objects.filter(shn__shp__product = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('date').annotate(Count('id')).order_by('date')
        chart_data = [(entry['date'], entry['id__count']) for entry in raw_data]
        all_external_visit_count = sum([e[1] for e in chart_data])
        
        schart_data = [chart_data]
        
        raw_data = ExternalVisit.objects.filter(shn__shp__product = product, shn__store = store, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('date').annotate(Count('id')).order_by('date')
        chart_data = [(entry['date'], entry['id__count']) for entry in raw_data]

        store_external_visit_count = sum([e[1] for e in chart_data])

        schart_data.append(chart_data)
        generate_timelapse_chart(schart_data, start_date, end_date, ['Clicks totales', 'Clicks a ' + unicode(store)], 'unit_' + str(shp.id) + '_02.png', u'Número de clicks a tiendas')
        
        # Third chart
        
        raw_data = ExternalVisit.objects.filter(shn__shp__product = product, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('shn__store').annotate(Count('id'))
        chart_data = [(unicode(Store.objects.get(pk = pair['shn__store'])), pair['id__count']) for pair in raw_data]
        
        generated_pie_chart = generate_pie_chart(chart_data, 'unit_' + str(shp.id) + '_03.png', u'Distribución de clicks entre tiendas')
        
        # Fourth chart
        
        raw_data = SponsoredVisit.objects.filter(shp = shp, date__gte = start_date, date__lt = end_date + timedelta(days = 1)).values('date').annotate(Count('id')).order_by('date')
        chart_data = [(entry['date'], entry['id__count']) for entry in raw_data]
        
        sponsored_visit_count = sum([e[1] for e in chart_data])

        generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de visitas patrocinadas'], 'unit_' + str(shp.id) + '_04.png', u'Número de visitas patrocinadas')
    else:
        product_visit_count = 0
        store_external_visit_count = 0
        all_external_visit_count = 0
        sponsored_visit_count = 0
        generated_pie_chart = False
    
    product = shp.product

    return append_store_metadata_to_response(request, 'store/entity_details.html', {
        'store': store,
        'shpe': shpe,
        'shp': shp,
        'other_shpes': other_shpes,
        'product': product,
        'form': form,
        'tag': random.randint(1, 1000000),
        'product_prices': product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price'),
        'product_visit_count': product_visit_count,
        'store_external_visit_count': store_external_visit_count,
        'all_external_visit_count': all_external_visit_count,
        'sponsored_visit_count': sponsored_visit_count,
        'generated_pie_chart': generated_pie_chart,
    })
    
@store_user_required
def entity_refresh_price(request, shpe_id):
    store = request.user.get_profile().assigned_store
    shpe = StoreHasProductEntity.objects.get(pk = shpe_id)
    
    if shpe.store != store:
        url = reverse('solonotebooks.cotizador.views_store.index')
        return HttpResponseRedirect(url)
        
    shpe.update_price()
    shpe.save()
    
    request.flash['message'] = 'Precio actualizado'
    
    url = reverse('solonotebooks.cotizador.views_store.entity_details', args = [shpe.id])
    return HttpResponseRedirect(url)
    
@store_user_required
def competition_report_excel(request):
    try:
        form, store, results = _competition_data(request)
    except:
        request.flash['error'] = 'Usted no tiene permisos para descargar este informe'
        return HttpResponseRedirect(reverse('solonotebooks.cotizador.views_store.registry'))

    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=informe_competitividad_%s.xls' % str(date.today())
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Informe')
    
    ws.col(0).width = 4000
    ws.col(1).width = 15000
    ws.col(2).width = 4000
    ws.col(3).width = 8000
    
    ws.row(0).height = 500
    
    bold_template = easyxf('font: bold True;')
    hyperlink_template = easyxf('font: underline single;')
    
    current_row = 0
    ws.write(current_row, 0, u'Informe de Competitividad',
        easyxf('font: bold True, height 300;'))
        
    current_row += 2
    ws.write(current_row, 0, 'Tienda', bold_template)
    ws.write(current_row, 1, unicode(store))
    current_row += 1
    ws.write(current_row, 0, 'Fecha', bold_template)
    ws.write(current_row, 1, unicode(date.today()))
    current_row += 1
    ws.write(current_row, 0, 'Ordenamiento', bold_template)
    ws.write(current_row, 1, unicode(form.get_ordering_as_string()))
    current_row += 2
    
    ws.write(current_row, 0, u'Código', bold_template)
    ws.write(current_row, 1, 'Nombre', bold_template)
    ws.write(current_row, 2, 'Precio Magens', bold_template)
    ws.write(current_row, 3, 'Mejor precio competencia', bold_template)
    current_row += 1
    
    for result in results:
        if result[1]:
            ws.write(current_row, 0, result[0])
            current_row += 1
            
            for entry in result[1]:
                ws.write(current_row, 0, entry.part_number)
                ws.write(current_row, 1, Formula('HYPERLINK("%s";"%s")' % ('%s%s' % (settings.SERVER_NAME, reverse('solonotebooks.cotizador.views_services.product_details', args = [entry.id])), unicode(entry))), hyperlink_template)
                ws.write(current_row, 2, Formula('HYPERLINK("%s";"%s")' % (entry.store_shpe.url, entry.store_shpe.pretty_price())), hyperlink_template)
                if entry.competitor_shpe:
                   ws.write(current_row, 3, Formula('HYPERLINK("%s";"%s (%s)")' % (entry.competitor_shpe.url, entry.competitor_shpe.pretty_price(), unicode(entry.competitor_shpe.store))), hyperlink_template)
                else:
                    ws.write(current_row, 3, u'Sólo disponible en %s' % unicode(store))
                current_row += 1

    wb.save(response)
    return response
