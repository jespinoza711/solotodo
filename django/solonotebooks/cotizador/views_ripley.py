from datetime import date
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from solonotebooks.cotizador.forms.ripley_notebook_search_form import RipleyNotebookSearchForm
from solonotebooks.cotizador.models.notebook import Notebook
from solonotebooks.cotizador.models.store_has_product import StoreHasProduct
from solonotebooks.cotizador.models.store_product_history import StoreProductHistory

considered_store_ids = [
    30,     # AbcDin
    9,      # Falabella
    18,     # Ripley
    11,     # Paris
    12      # PCFactory
]

epoch = date(1970, 1, 1)

def milliseconds_since_epoch(date):
    return long(1000 * (date - epoch).days * (60*60*24))

def index(request):
    return HttpResponseRedirect('/ripley/notebooks/')

def notebooks(request):
    form = RipleyNotebookSearchForm(request.GET)
    notebooks = form.notebook_list()

    return render_to_response('ripley/index.html', {
        'form': form,
        'notebooks': notebooks
    })

def notebook_details(request, notebook_id):
    notebook = Notebook.objects.get(pk=notebook_id)

    notebook_shps = StoreHasProduct.objects.filter(
        shpe__isnull=False,
        product=notebook,
        shpe__store__id__in=considered_store_ids
    ).order_by('shpe__latest_price')

    return render_to_response('ripley/notebook_details.html', {
        'notebook': notebook,
        'notebook_shps': notebook_shps
    })

def notebook_details_json(request, notebook_id):
    notebook = Notebook.objects.get(pk=notebook_id)

    sphs = list(StoreProductHistory.objects.filter(
        registry__shp__product=notebook,
        registry__store__in=considered_store_ids
    ).order_by('registry__store', 'date'))

    result = {}
    current_list = list()
    last_store = sphs[0].registry.store.name

    for sph in sphs:
        if sph.registry.store.name != last_store:
            result[last_store] = current_list
            current_list = list()
            last_store = sph.registry.store.name

        current_list.append([milliseconds_since_epoch(sph.date), sph.price])

    last_sph = sphs[-1]
    if last_sph.registry.store.name not in result:
        result[last_sph.registry.store.name] = current_list

    highcharts_result = []

    for store_name, price_history in result.items():
        subresult = dict()
        subresult['name'] = store_name
        subresult['data'] = price_history
        highcharts_result.append(subresult)

    return HttpResponse(json.dumps(highcharts_result), content_type='application/json')

