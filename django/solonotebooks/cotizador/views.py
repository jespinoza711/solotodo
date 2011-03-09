#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import operator
import urllib
from datetime import date, timedelta
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
    
# Main landing page (/)    
def index(request):
    ptypes = ProductType.objects.all()
    highlighted_products_form = HighlightedProductsForm.initialize(request.GET)
    result_products = highlighted_products_form.apply_filter(Product.get_valid())[:10]
    
    return append_ads_to_response(request, 'cotizador/index.html', {
        'hnf': highlighted_products_form,
        'products': result_products,
        'ptype': None,
        
        'ptypes': ptypes,
    })
    
def product_type_index(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()
    
    highlighted_products_form = HighlightedProductsForm.initialize(request.GET)
    base_products = product_type_class.get_valid()
    result_products = highlighted_products_form.apply_filter(base_products)[:10]
    
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

    search_form = initialize_search_form(request.GET, ptype)
    search_form.save()
    
    # Grab all the candidates (those currently available)
    result_products = search_form.filter_products(product_type_class.get_valid())
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

    d = dict(search_form.price_choices)
    
    return append_ads_to_response(request, 'cotizador/catalog.html', {
        'form': search_form,
        'max_price': d[str(search_form.max_price)], 
        'min_price': d[str(search_form.min_price)],
        'remove_filter_links': search_form.generate_remove_filter_links(),
        'num_results': num_results,
        'first_result_index': first_result_index,
        'last_result_index': last_result_index,
        'products': result_products,
        'current_url': search_form.generate_url_without_ordering(),
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
    
    shps = []
    
    shpes = StoreHasProductEntity.objects.filter(store = store).filter(is_available = True, is_hidden = False).order_by('latest_price')
    
    for shpe in shpes:
        if shpe.shp and shpe.shp not in shps:
            shps.append(shpe.shp)
    
    for shp in shps:
        shp.product = shp.product.get_polymorphic_instance()
        shp.product.shp = shp
        
    return append_ads_to_response(request, 'cotizador/store_details.html', {
        'store': store,
        'shps': shps,
        'ptype': ProductType.default()
    })
    
# View for showing all of the stores currently in the DB    
def store_index(request):
    stores = Store.objects.all()
    return append_ads_to_response(request, 'cotizador/store_index.html', {
        'stores': stores,
        'ptype': ProductType.default()
    })  
    
def search(request):
    ptype = None
    url = reverse('solonotebooks.cotizador.views.index')
    
    try:
        if 'product_type' in request.GET:
            ptype = ProductType.objects.get(urlname = request.GET['product_type'])

    except:
        return HttpResponseRedirect(url)
        
    if ptype:
        url = reverse('solonotebooks.cotizador.views.product_type_index', kwargs = {'product_type_urlname': ptype.urlname})
    else:
        url = reverse('solonotebooks.cotizador.views.index')
    
    try:
        product_type_class = ptype.get_class()
    except:
        product_type_class = Product

    try:    
        query = request.GET['search_keywords']
        if not query:
            return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect(url)
    
    # We grab all the candidates (those currently available)
    available_products = product_type_class.get_valid()
    
    # For each one, we assign a score base on how many of the keywords match a 
    # huge single line description of the product stored in the DB
    result_products = [[prod, stringCompare(prod.long_description, query)] for prod in available_products]
    # If the hit is too low (< 10%) they are eliminated
    result_products = filter(lambda(x): x[1] > 10, result_products) 
    # Finally we sort them from highest to lowest hit rate
    result_products = sorted(result_products, key = operator.itemgetter(1), reverse = True)
    
    page_count = int(ceil(len(result_products) / 10.0))
    
    try:
        page_number = int(request.GET['page_number'])
    except:
        page_number = 1
        
    pages = filter(lambda(x): x > 0 and x <= page_count, range(page_number - 3, page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
        
    result_products = result_products[(page_number - 1) * 10 : page_number * 10]
    
    for result in result_products:
        result[0].matching = result[1]
        
    result_products = [result[0] for result in result_products]
    
    if ptype:
        template = 'cotizador/search.html'
    else:
        template = 'cotizador/search_no_product_type.html'
    
    return append_ads_to_response(request, template, {
        'query': query,
        'products': result_products,
        'page_number': page_number,
        'prev_page': page_number - 1,
        'post_page': page_number + 1,
        'page_count': page_count,
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,        
        'ptype': ptype,
        'ptypes': ProductType.objects.all()
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
    args['server_name'] = settings.SERVER_NAME
    args['settings'] = settings
    
    if 'PATH_INFO' in request.META:
        next = urlquote(request.META['PATH_INFO'])
        next += concat_dictionary(request.GET)
            
        args['next'] = next
        
    if 'signup_key' not in request.session:
        request.session['signup_key'] = int(time())
        
    if 'ptype' in args:
        ptype = args['ptype']
    else:
        ptype = ProductType.default()
        
    if 'form' not in args:
        args['form'] = initialize_search_form(request.GET, ptype)
        
    
    try:    
        args['change_category_url'] = args['form'].generate_url_without_main_category()        
        search_form = args['form']
        main_category_choices = [Category()]
        main_category_choices.extend(list(search_form.main_category().choices.queryset))
        args['main_category_choices'] = main_category_choices
            
        main_category_comparison_key = search_form.main_category_key()
        args['main_category_comparison_key'] = main_category_comparison_key
    except:
        pass

        
    args['signup_key'] = request.session['signup_key']
    args['site_name'] = settings.SITE_NAME
    
    return render_to_response(template, args)
    
# View for displaying every single product in the DB
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
            'ptype': ProductType.default()
        })
    
# View that gets called when a user clicks an external link to a store
# we log this for statistical purposes and... maybe build a business model
# someday...
def store_product_redirect(request, store_product_id):
    store_product = get_object_or_404(StoreHasProductEntity, pk = store_product_id)
    if not request.user.is_staff:
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
            product_comment.product = product
            if not request.user.is_anonymous():
                product_comment.user = request.user
                product_comment.validated = True
            else:
                product_comment.nickname = commentForm.cleaned_data['nickname']
                request.session['posted_comment'] = True
                
            product_comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'] + '?refresh=true');
    else:
        nv = ProductVisit()
        nv.product = product
        nv.save()
        commentForm = ProductCommentForm()

    posted_comment = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    # Find the stores with this product available
    stores_with_product_available = product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price')
        
    #similar_products_ids = product.similar_products.split(',')
    #similar_products = [Product.objects.get(pk = product_id) for product_id in similar_products_ids if product_id and int(product_id)]
    
    try:
        product_subscription = ProductSubscription.objects.filter(user = request.user, product = product, is_active = True)[0]
    except:
        product_subscription = None
    
    return append_ads_to_response(request, 'cotizador/product_details.html', {
        'product': product,
        'comment_form': commentForm,
        'product_prices': stores_with_product_available,
        'product_comments': product.productcomment_set.filter(validated = True).order_by('id'),
        'posted_comment': posted_comment,
        #'similar_products': similar_products,
        'subscription': product_subscription,
        'ptype': product.ptype
        })
