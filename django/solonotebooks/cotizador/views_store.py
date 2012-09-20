#-*- coding: UTF-8 -*-
from datetime import date, timedelta
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from solonotebooks import settings
from solonotebooks.cotizador.views import append_metadata_to_response
from solonotebooks.cotizador.tasks import UpdateStore
from solonotebooks.cotizador.forms import DateRangeForm, SearchShpeForm, CompetitivityReportOrdering
from models import *
from exceptions import *
from utils import *
import xlwt
import random

def append_store_metadata_to_response(request, template, args):
    tabs = [
            u'Opciones',
            [
                    ['Registro', reverse('solonotebooks.cotizador.views_store.registry')],
                    ['Estadísticas', reverse('solonotebooks.cotizador.views_store.statistics')],
                    ['Resultados patrocinados', reverse('solonotebooks.cotizador.views_store.sponsored_results')],
                    ['Publicidad', reverse('solonotebooks.cotizador.views_store.advertisement_results')]
            ]
        ]

    args['tabs'] = tabs
    args['store'] = request.user.get_profile().assigned_store
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
def update_prices(request):
    store = request.user.get_profile().assigned_store
    
    if request.method == 'POST':
        registry = StoreCustomUpdateRegistry()
        registry.store = store
        registry.status = 'Pendiente'
        registry.save()
        UpdateStore.delay(registry)
        url = reverse('solonotebooks.cotizador.views_store.update_prices')
        return HttpResponseRedirect(url)
    
    update_registries = StoreCustomUpdateRegistry.objects.filter(store=store)
    return append_store_metadata_to_response(request, 'store/update_prices.html', {
            'store': store,
            'update_registries': update_registries,
        })
    
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
            request.flash['error'] = 'Por favor seleccione un rango de fechas valido'
            url = reverse('solonotebooks.cotizador.views_store.entity_details', args = [shpe.id])
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
    
    ws.col(0).width = 3000
    ws.col(1).width = 7000
    ws.col(2).width = 5000
    ws.col(3).width = 16000
    ws.col(4).width = 5000
    ws.col(5).width = 5000
    ws.col(6).width = 5000
    ws.col(7).width = 5000
    ws.col(8).width = 5000
    ws.col(9).width = 5000
    ws.col(10).width = 5000
    ws.col(11).width = 5000
    ws.col(12).width = 5000
    
    current_row = 0
    ws.write(current_row, 0, u'Relevancia')
    ws.write(current_row, 1, u'Tipo relevancia')
    ws.write(current_row, 2, u'Código')
    ws.write(current_row, 3, u'Nombre')
    ws.write(current_row, 4, u'Categoría')
    ws.write(current_row, 5, u'Precio %s' % unicode(store))
    ws.write(current_row, 6, u'Competencia 1')
    ws.write(current_row, 7, u'Competidor 1')
    ws.write(current_row, 8, u'Competencia 2')
    ws.write(current_row, 9, u'Competidor 2')
    ws.write(current_row, 10, u'Competencia 3')
    ws.write(current_row, 11, u'Competidor 3')
    current_row += 1
    
    for result in results:
        if result[1]:
            for idx, entry in enumerate(result[1]):
                ws.write(current_row, 0, str(idx + 1))
                ws.write(current_row, 1, form.get_ordering_as_string())
                ws.write(current_row, 2, entry.part_number)
                ws.write(current_row, 3, unicode(entry))
                ws.write(current_row, 4, result[0])
                ws.write(current_row, 5, str(entry.store_shpe.latest_price))
                
                
                for idx, shp in enumerate(entry.competitor_shps):
                   ws.write(current_row, 6 + 2 * idx, str(shp.shpe.latest_price))
                   ws.write(current_row, 6 + 2 * idx + 1,  unicode(shp.shpe.store))   
                    
                
                current_row += 1

    wb.save(response)
    return response

@store_user_required
def sponsored_results(request):
    form, start_date, end_date = get_and_clean_form(request.GET)

    sponsored_visits = SponsoredVisit.objects.filter(
        shp__shpe__store=request.user.get_profile().assigned_store,
        date__gte=start_date,
        date__lte=end_date
    )

    if request.GET.get('format', 'html') == 'json':
        data = sponsored_visits.values('date').annotate(data=Count('id')).order_by('date')

        def label_function(ev):
            return u'Número de clicks'

        def f(start_date, end_date):
            return fill_timelapse(data, start_date, end_date,
                label_function)

        chart_data = line_chart_data(
            start_date, end_date, f)

        return HttpResponse(simplejson.dumps(chart_data))
    else:
        clicks_per_store_data = sponsored_visits.values('shp__product').annotate(data=Count('id')).order_by('shp__product')

        clicks_per_store = [(Product.objects.get(pk=e['shp__product']), e['data']) for e in clicks_per_store_data]
        clicks_per_store = sorted(clicks_per_store, key=lambda x: x[1], reverse=True)

        return append_store_metadata_to_response(request, 'store/sponsored_results.html', {
            'form': form,
            'total_clicks': sponsored_visits.count(),
            'clicks_per_store': clicks_per_store
            })

@store_user_required
def advertisement_results(request):
    form, start_date, end_date = get_and_clean_form(request.GET)

    advertisement_impressions = AdvertisementImpression.objects.filter(
        advertisement__store=request.user.get_profile().assigned_store,
        date__gte=start_date,
        date__lte=end_date
    )

    advertisement_visits = AdvertisementVisit.objects.filter(
        advertisement__store=request.user.get_profile().assigned_store,
        date__gte=start_date,
        date__lte=end_date
    )

    data = advertisement_visits.values('date').annotate(data=Count('id')).order_by('date')

    def label_function(ev):
        return u'Número de clicks'

    def f(start_date, end_date):
        return fill_timelapse(data, start_date, end_date,
            label_function)

    chart_data = line_chart_data(
        start_date, end_date, f)

    data = advertisement_impressions.values('date').annotate(data=Count('id')).order_by('date')

    def label_function(ev):
        return u'Número de impresiones'

    def f(start_date, end_date):
        return fill_timelapse(data, start_date, end_date,
            label_function)

    chart_data.extend(line_chart_data(
        start_date, end_date, f))

    chart_data[0]['yAxis'] = 1
    chart_data[1]['yAxis'] = 0

    total_visits = advertisement_visits.count()
    total_impressions = 0

    advertisement_visits = advertisement_visits.values('advertisement').annotate(data=Count('id')).order_by('advertisement')
    advertisement_visits_dict = dict([(e['advertisement'], e['data']) for e in advertisement_visits])

    advertisement_impressions = advertisement_impressions.values('advertisement').annotate(data=Count('id')).order_by('advertisement')
    advertisement_impressions_dict = dict([(e['advertisement'], e['data']) for e in advertisement_impressions])

    advertisements = Advertisement.objects.filter(
        store=request.user.get_profile().assigned_store
    )

    result_data = []

    for ad in advertisements:
        clicks = advertisement_visits_dict.get(ad.id, 0)
        impressions = advertisement_impressions_dict.get(ad.id, 0)

        total_impressions += impressions

        if impressions == 0:
            ratio = 0
        else:
            ratio = 100.0 * clicks / impressions

        result_data.append((ad, clicks, ratio))

    return append_store_metadata_to_response(request, 'store/advertisement_results.html', {
        'form': form,
        'result_data': result_data,
        'total_visits': total_visits,
        'total_impressions': total_impressions,
        'chart_data': simplejson.dumps(chart_data)
    })
