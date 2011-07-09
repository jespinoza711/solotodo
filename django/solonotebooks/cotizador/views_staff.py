#-*- coding: UTF-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Count
from models import *
from fields import *
from utils import *
from views import *
from forms import *
import random

def staff_login_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/account/login')
            
        if (request.user.is_staff and request.user.id == int(kwargs['staff_id'])) or request.user.is_superuser:
            kwargs['staff'] = User.objects.get(pk=kwargs['staff_id'])
            del kwargs['staff_id']
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/account/login')
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
def append_staff_ptype_to_response(request, template, args):
    tabs = []
    uid = args['staff'].id
    
    name = 'Nuevas entidades'
    url = reverse('solonotebooks.cotizador.views_staff.new_entities', args=[uid])
    tabs.append([-1, name, url])
    
    name = 'Estadísticas'
    url = reverse('solonotebooks.cotizador.views_staff.statistics', args=[uid])
    tabs.append([-1, name, url])
    
    
    args['tabs'] = ['Staff', tabs]
    return append_metadata_to_response(request, template, args)
    
@staff_login_required
def new_entities(request, staff):
    # Shows the models that don't have an associated product in the DB (i.e.: pending)
    managed_product_types = staff.get_profile().managed_product_types.all()
    pending_shpes = []
    for ptype in managed_product_types:
        pending_shpe = [ptype, StoreHasProductEntity.objects.filter(is_hidden = False, is_available = True, shp__isnull = True, ptype = ptype)]
        pending_shpes.append(pending_shpe)
        
    return append_staff_ptype_to_response(request, 'staff/new_entities.html', {
            'pending_shpes': pending_shpes,
            'staff': staff,
        })
        
@staff_login_required
def storehasproductentity_edit(request, staff, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    
    if not shpe.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
        return HttpResponseRedirect(url)

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
                
            shpe.resolved_by = staff
            shpe.save()
                
            shp.update(recursive = True)
            url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
            return HttpResponseRedirect(url)
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
        
    return append_staff_ptype_to_response(request, 'staff/store_has_product_entity_edit.html', {
        'shpe_form': form,
        'shpe': shpe,
        'options': options,
        'staff': staff,
    })
    
@staff_login_required
def storehasproductentity_hide(request, staff, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    
    if not shpe.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
        return HttpResponseRedirect(url)
    
    shpe.is_hidden = True
    shpe.save()
    shpe.update(recursive = True)
    url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
    return HttpResponseRedirect(url);
    
@staff_login_required
def storehasproductentity_show(request, staff, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    
    if not shpe.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
        return HttpResponseRedirect(url)
    
    shpe.is_hidden = False
    shpe.save()
    shpe.update(recursive = True)
    url = reverse('solonotebooks.cotizador.views_staff.storehasproductentity_edit', args = [staff.id, shpe.id])    
    return HttpResponseRedirect(url);
    
@staff_login_required
def storehasproductentity_refresh_price(request, staff, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    
    if not shpe.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
        return HttpResponseRedirect(url)
    
    shpe.update_price()
    shpe.save()
    url = reverse('solonotebooks.cotizador.views_staff.storehasproductentity_edit', args = [staff.id, shpe.id])
    return HttpResponseRedirect(url)
    
@staff_login_required
def polymorphic_admin_request(request, staff, product_id):
    product = Product.objects.get(pk = product_id)
    
    if not product.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views.index')
        return HttpResponseRedirect(url)
    
    url = '/admin/cotizador/' + product.ptype.adminurlname + '/' + str(product.id)
    return HttpResponseRedirect(url)
    
@staff_login_required
def clone_product(request, staff, product_id):
    product = Product.objects.get(pk = product_id).get_polymorphic_instance()
    
    if not product.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views.index')
        return HttpResponseRedirect(url)
    
    cloned_product = product.clone_product()
    
    url = reverse('solonotebooks.cotizador.views_staff.polymorphic_admin_request', args = [staff.id, cloned_product.id])
    return HttpResponseRedirect(url)
    
@staff_login_required
def storehasproductentity_change_ptype(request, staff, store_has_product_entity_id):
    shpe = get_object_or_404(StoreHasProductEntity, pk = store_has_product_entity_id)
    
    if not shpe.ptype in staff.get_profile().managed_product_types.all():
        url = reverse('solonotebooks.cotizador.views_staff.new_entities', args = [staff.id])
        return HttpResponseRedirect(url)
    
    ptype = ProductType.objects.get(classname = request.GET['classname'])
    shpe.ptype = ptype
    shpe.save()
    url = reverse('solonotebooks.cotizador.views_staff.storehasproductentity_edit', args = [staff.id, shpe.id])
    return HttpResponseRedirect(url);
    
@staff_login_required
def statistics(request, staff):
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
            url = reverse('solonotebooks.cotizador.views_staff.statistics')
            return HttpResponseRedirect(url)
    
    # First chart: Number of SHPEs resolved per day

    raw_data = StoreHasProductEntity.objects.filter(date_resolved__gte = start_date, date_resolved__lt = end_date + timedelta(days = 1), is_hidden = False, resolved_by = staff, shp__isnull = False).extra(select = {'d': 'CAST(date_resolved AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de entidades resueltas'], 'staff_%d_statistics_01.png' % staff.id, u'Número de nuevas entidades resueltas')
    
    shpes_resolved_count = sum([e[1] for e in chart_data])
    
    # Second chart: Number of products created per day
    
    raw_data = Product.objects.filter(date_added__gte = start_date, date_added__lt = end_date + timedelta(days = 1), created_by = staff).extra(select = {'d': 'CAST(date_added AS DATE)'}).values('d').annotate(Count('id')).order_by('d')
    chart_data = [(entry['d'], entry['id__count']) for entry in raw_data]
    generate_timelapse_chart([chart_data], start_date, end_date, [u'Número de productos creados'], 'staff_%d_statistics_02.png' % staff.id, u'Número de productos creados')
    
    product_creation_count = sum([e[1] for e in chart_data])
    
    return append_staff_ptype_to_response(request, 'staff/statistics.html', {
            'form': form,
            'shpes_resolved_count': shpes_resolved_count,
            'product_creation_count': product_creation_count,
            'tag': random.randint(1, 1000000),
            'staff': staff,
        })

