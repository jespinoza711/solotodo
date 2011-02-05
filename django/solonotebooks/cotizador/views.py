#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import operator
import simplejson, urllib
from datetime import date, timedelta
from time import time
from math import ceil
from django.db.models import Min, Max, Q
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson 
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
    
# Main landing page (/)    
def index(request):
    url = reverse('cotizador.views.product_type_index', kwargs = {'product_type_urlname': 'notebooks'})
    return HttpResponseRedirect(url)
    
def search(request):
    url = reverse('cotizador.views.product_type_search', kwargs = {'product_type_urlname': 'notebooks'})
    url += concat_dictionary(request.GET)
    return HttpResponseRedirect(url)
    
def product_type_index(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()
    
    highlighted_products_form = HighlightedProductsForm.initialize(request.GET)
    result_products = highlighted_products_form.apply_filter(product_type_class.get_valid())[:10]
    
    return append_ads_to_response(request, 'cotizador/product_type_index.html', {
        'hnf': highlighted_products_form,
        'products': result_products,
        'product_type_class': product_type_class,
        'ptype': ptype
    })
    
# View that handles the main catalog, applying filters and ordering
# (/catalog)
def product_type_catalog(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()

    search_form = initialize_search_form(request.GET)
    search_form.save()
    
    # Grab all the candidates (those currently available)
    result_products, ordering_direction = filter_notebooks(product_type_class.get_valid(), search_form)
    num_results = len(result_products)
    
    page_count = ceil(len(result_products) / 10.0);        
    
    pages = filter(lambda(x): x > 0 and x <= page_count, range(search_form.page_number - 3, search_form.page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
    
    first_result_index = (search_form.page_number - 1) * 10 + 1
    last_result_index = search_form.page_number * 10
    if last_result_index > num_results:
        last_result_index = num_results
    result_products = result_products[first_result_index - 1 : last_result_index]
    
    product_link_args = search_form.generateProdutLinkArgs()
    '''
    publicized_notebooks = Notebook.objects.filter(is_available = True).filter(~Q(publicized_offer = None))
    
    result_publicized_notebooks, ordering_direction =  filter_notebooks(publicized_notebooks, search_form)
    
    chosen_publicized_notebooks = []
    
    insert_positions = [2, 7]
    counter = 0
    for publicized_notebook in result_publicized_notebooks:
        if publicized_notebook not in result_notebooks:
            publicized_notebook.is_publicized = True
            publicized_notebook.url = '/store_notebook/' + str(publicized_notebook.publicized_offer.id)
            result_notebooks.insert(insert_positions[counter], publicized_notebook)
            counter += 1
            if counter == len(insert_positions):
                break
    '''
    d = dict(NotebookSearchForm.price_choices)
    
    return append_ads_to_response(request, 'cotizador/catalog.html', {
        'form': search_form,
        'max_price': d[str(search_form.max_price)], 
        'min_price': d[str(search_form.min_price)],
        'remove_filter_links': search_form.generate_remove_filter_links(),
        'change_ntype_url': search_form.generate_url_without_ntype(),
        'num_results': num_results,
        'first_result_index': first_result_index,
        'last_result_index': last_result_index,
        'products': result_products,
        'current_url': search_form.generateUrlWithoutOrdering(),
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'left_page': left_page,
        'right_page': right_page,
        'page_range': pages,
        'ordering': str(search_form.ordering),
        'ptype': ptype
    })
    
# View for showing a particular store with the products it offers    
def store_details(request, store_id):
    store = get_object_or_404(Store, pk = store_id)
    shps = StoreHasProduct.objects.filter(store = store).filter(shpe__isnull = False).order_by('shpe__latest_price')
    
    for shp in shps:
        shp.product = shp.product.get_polymorphic_instance()
        shp.product.min_price = shp.shpe.latest_price
        
    return append_ads_to_response(request, 'cotizador/store_details.html', {
        'store': store,
        'shps': shps,
        'ptype': ProductType.objects.get(urlname = 'notebooks')
    })
    
# View for showing all of the stores currently in the DB    
def store_index(request):
    stores = Store.objects.all()
    return append_ads_to_response(request, 'cotizador/store_index.html', {
        'stores': stores,
        'ptype': ProductType.objects.get(urlname = 'notebooks')
    })  
    
def product_type_search(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()

    url = reverse('cotizador.views.product_type_index', kwargs = {'product_type_urlname': ptype.urlname})
        
    try:
        query = request.GET['search_keywords']
        if not query:
            return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect(url)
    
    # We grab all the candidates (those currently available)
    available_products = product_type_class.get_valid()
    
    # For each one, we assign a score base on how many of the keywords match a 
    # huge single line description of the notebook stored in the DB
    result_products = [[ntbk, stringCompare(ntbk.long_description, query)] for ntbk in available_products]
    # If the hit is too low (< 10%) they are eliminated
    result_products = filter(lambda(x): x[1] > 10, result_products) 
    # Finally we sort them from highest to lowest hit rate
    result_products = sorted(result_products, key = operator.itemgetter(1), reverse = True)
    
    # Boilerplate code for setting up the links to each page of the results
    search_form = initialize_search_form(request.GET)
    
    page_count = ceil(len(result_products) / 10.0);
        
    pages = filter(lambda(x): x > 0 and x <= page_count, range(search_form.page_number - 3, search_form.page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
        
    result_products = result_products[(search_form.page_number - 1) * 10 : search_form.page_number * 10]
    
    for result in result_products:
        result[0].matching = result[1]
        
    result_products = [result[0] for result in result_products]
    
    return append_ads_to_response(request, 'cotizador/search.html', {
        'form': search_form,
        'query': query,
        'products': result_products,
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,        
        'ptype': ptype
    })
    
def append_ads_to_response(request, template, args):
    args['side_ad'] = load_advertisement('Side')
    args['top_ad'] = load_advertisement('Top')
    
    return append_user_to_response(request, template, args)
    
class Category:
    def __init__(self):
        self.id = 0
        
    def __unicode__(self):
        return u'Todos'
    
def append_user_to_response(request, template, args):
    authenticated_user = False
    username = ''
    
    if request.user.is_authenticated():
        authenticated_user = True
        username = request.user.username
        
    args['user'] = request.user
    args['authenticated_user'] = authenticated_user
    args['flash'] = request.flash
    args['username'] = username
    if 'PATH_INFO' in request.META:
        next = urlquote(request.META['PATH_INFO'])
        next += concat_dictionary(request.GET)
            
        args['next'] = next
        
    if 'signup_key' not in request.session:
        request.session['signup_key'] = int(time())
        
    if 'form' not in args:
        args['form'] = initialize_search_form(request.GET)
        
    search_form = args['form']
    main_category_choices = [Category()]
    main_category_choices.extend(list(search_form.main_category().choices.queryset))
    args['main_category_choices'] = main_category_choices
        
    main_category_comparison_key = search_form.main_category_key()
    
    args['main_category_comparison_key'] = main_category_comparison_key
    args['signup_key'] = request.session['signup_key']
    args['site_name'] = settings.SITE_NAME
    
    return render_to_response(template, args)
    
# View for displaying every single notebook in the DB
def all_products(request):
    result = []
    product_types = ProductType.objects.all()
    
    for product_type in product_types:
        step = []
        c = product_type.get_class()
        step.append(product_type.displayname)
        step.append(c.objects.all())
        result.append(step)

    return append_ads_to_response(request, 'cotizador/all_products.html',
        {
            'product_types': result,
            'ptype': ProductType.objects.get(urlname = 'notebooks')
        })
    
# View that gets called when a user clicks an external link to a store
# we log this for statistical purposes and... maybe build a business model
# someday...
def store_product_redirect(request, store_product_id):
    store_product = get_object_or_404(StoreHasProductEntity, pk = store_product_id)
    external_visit = ExternalVisit()
    external_visit.shpe = store_product
    external_visit.date = date.today()
    external_visit.save()
    return HttpResponseRedirect(store_product.url)
    
# View that gets called when a user clicks an ad
def ad_visited(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk = advertisement_id)
    ad_visit = AdvertisementVisit()
    if 'HTTP_REFERER' in request.META:
        ad_visit.referer_url = request.META['HTTP_REFERER']
    else:
        ad_visit.referer_url = ''
    ad_visit.advertisement = advertisement
    ad_visit.save()
    return HttpResponseRedirect(advertisement.target_url)
    
# View in charge of showing the details of a product and handle commment submissions        
def product_details(request, product_id):
    product = get_object_or_404(Product, pk = product_id).get_polymorphic_instance()
    
    # If this is a comment submission, validate and save
    if request.method == 'POST': 
        commentForm = ProductCommentForm(request.POST)
        if commentForm.is_valid():
            product_comment = ProductComment()
            product_comment.date = date.today()        
            rawComment = commentForm.cleaned_data['comments']
            product_comment.comments = rawComment.replace('\n', '<br />')
            product_comment.notebook = product
            if not request.user.is_anonymous():
                product_comment.user = request.user
                product_comment.validated = True
            else:
                product_comment.nickname = commentForm.cleaned_data['nickname']
                request.session['posted_comment'] = True
                
            product_comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER']);
    else:
        nv = ProductVisit()
        nv.notebook = product
        nv.save()
        commentForm = ProductCommentForm()

    posted_comment = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    # Find the stores with this notebook available
    stores_with_product_available = product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price')
        
    similar_products_ids = product.similar_products.split(',')
    similar_products = [Product.objects.get(pk = product_id) for product_id in similar_products_ids if product_id]
    
    try:
        product_subscription = ProductSubscription.objects.filter(user = request.user, product = product, is_active = True)[0]
    except:
        product_subscription = None
    
    return append_ads_to_response(request, 'cotizador/' + product.ptype.adminurlname + '_details.html', {
        product.ptype.adminurlname: product,
        'comment_form': commentForm,
        'product_prices': stores_with_product_available,
        'product_comments': product.productcomment_set.filter(validated = True).order_by('id'),
        'posted_comment': posted_comment,
        'similar_products': similar_products,
        'subscription': product_subscription,
        'ptype': product.ptype
        })

'''    
def add_item_notebook_comparison(request):
    try:
        if not 'comparison_list' in request.session:
            request.session['comparison_list'] = NotebookComparisonList()
            request.session['comparison_list'].save()
        
        ntbk = Notebook.objects.get(pk = request.POST['ntbk_id'])
        request.session['comparison_list'].notebooks.add(ntbk)
        request.session['comparison_list'].save()
        
        response = {'code': 'OK'}
    except:
        response = {'code': 'Error'}
    
    request.session.modified = True
    
    data = simplejson.dumps(response, indent = 4)
    return HttpResponse(data, mimetype='application/javascript') 


def remove_item_notebook_comparison(request):
    try:
        if not 'comparison_list' in request.session:
            request.session['comparison_list'] = NotebookComparisonList()
            request.session['comparison_list'].save()
        
        ntbk = Notebook.objects.get(pk = request.POST['ntbk_id'])
        request.session['comparison_list'].notebooks.remove(ntbk)
        request.session['comparison_list'].save()
        
        response = {'code': 'OK'}
    except:
        response = {'code': 'Error'}
    
    request.session.modified = True
    
    data = simplejson.dumps(response, indent = 4)
    return HttpResponse(data, mimetype='application/javascript') 
    
def notebook_comparison(request):
    if request.method == 'POST' or not 'comparison_list' in request.session:
        request.session['comparison_list'] = NotebookComparisonList()
        request.session['comparison_list'].save()        
        
    return append_ads_to_response(request, 'cotizador/notebook_comparison.html', {
        'notebooks': request.session['comparison_list'].notebooks.all(),
        'comparison_list_id': request.session['comparison_list'].id,
        'server_name': settings.SERVER_NAME
    })
    
def notebook_comparison_details(request, comparison_id):
    comparison = get_object_or_404(NotebookComparisonList, pk = comparison_id)
    return append_ads_to_response(request, 'cotizador/comparison_details.html', {
        'notebooks': comparison.notebooks.all(),
    })
'''
