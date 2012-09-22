#-*- coding: UTF-8 -*-
import operator
import re
from datetime import date
from time import time
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlquote
from solonotebooks import settings
from solonotebooks.cotizador.forms import *
from models import *
from exceptions import *
from utils import *
    
# Main landing page (/)    
def index(request):
    highlighted_products_form = HighlightedProductsForm.initialize(request.GET)
    result_products = highlighted_products_form.apply_filter(Product.get_available())[:10]
    
    return append_metadata_to_response(request, 'cotizador/index.html', {
        'hnf': highlighted_products_form,
        'products': result_products,
        'ptypes': ProductType.objects.all(),
    })
    
def product_type_index(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()
    
    highlighted_products_form = HighlightedProductsForm.initialize(request.GET)
    base_products = product_type_class.get_available()
    result_products = highlighted_products_form.apply_filter(base_products)[:10]
    
    return append_metadata_to_response(request, 'cotizador/product_type_index.html', {
        'hnf': highlighted_products_form,
        'products': result_products,
        'ptype': ptype
    })
    
def product_type_catalog(request, product_type_urlname):
    ptype = get_object_or_404(ProductType, urlname = product_type_urlname)
    product_type_class = ptype.get_class()

    search_form = initialize_search_form(request, ptype)
    search_form.save()
    
    result_products = search_form.filter(product_type_class)
    num_results = len(result_products)
    
    page_count = ceil(len(result_products) / 10.0)
    
    pages = filter(lambda(x): x > 0 and x <= page_count, range(search_form.page_number - 3, search_form.page_number + 3))
    try:
        left_page = pages[0]
    except IndexError:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except IndexError:
        right_page = 0

    all_sponsored_products = product_type_class.get_available().filter(sponsored_shp__isnull = False)
    try:
        sponsored_product = search_form.filter_products(all_sponsored_products)[search_form.page_number - 1]
        sponsored_product.is_sponsored = True
    except IndexError:
        sponsored_product = None
    
    first_result_index = (search_form.page_number - 1) * 10 + 1
    last_result_index = search_form.page_number * 10
    if last_result_index > num_results:
        last_result_index = num_results

    result_products = result_products[first_result_index - 1 : last_result_index]
    result_products = filter(lambda x: x != sponsored_product, result_products)

    if sponsored_product:
        result_products.insert(0, sponsored_product)
        
    d = dict(search_form.price_choices)
    
    return append_metadata_to_response(request, 'cotizador/catalog.html', {
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
    available_products = product_type_class.get_available()
    
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
        result[0].matching = str(result[1]) + '%'
        
    result_products = [result[0] for result in result_products]
    
    if ptype:
        template = 'cotizador/search.html'
    else:
        template = 'cotizador/search_no_product_type.html'
    
    return append_metadata_to_response(request, template, {
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
        'ptypes': ProductType.get_valid()
    })
    
def append_metadata_to_response(request, template, args):
    args['side_ad'] = load_advertisement('Side')
    args['top_ad'] = load_advertisement('Top')

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
        
    ptype = None
    if 'ptype' in args:
        ptype = args['ptype']
        
    if 'form' not in args:
        args['form'] = initialize_search_form(request, ptype)        
    
    try:
        url_extension = args['form'].generate_url_without_main_category()        
        search_form = args['form']
            
        main_category_comparison_key = search_form.main_category_key()
    except Exception, e:
        url_extension = ''
        main_category_comparison_key = 0
        
    args['main_category_comparison_key'] = main_category_comparison_key
    
    if 'tabs' not in args:
        from solonotebooks.cotizador.forms import *
        
        if ptype:
            classname = ptype.classname
            s_form = args['form']

            url = reverse('solonotebooks.cotizador.views.product_type_catalog', args = [ptype.urlname])
            tabs = [[0, 'Todos', url + '?' + url_extension]]
            
            options = s_form.main_category().choices.queryset
            for option in options:
                option_url = url + '?' + url_extension + '&' + s_form.main_category_string() + '=' + str(option.id)
                tabs.append([option.id, str(option), option_url])
                    
            args['tabs'] = ['Tipos de ' + ptype.displayname, tabs]
        else:
            '''
            tabs = []
            for ptype in ProductType.objects.all():
                tabs.append([ptype.id, ptype.indexname, reverse('solonotebooks.cotizador.views.product_type_catalog', args = [ptype.urlname])])
            tabs = ['', tabs]
            args['tabs'] = tabs
            '''
    
    args['signup_key'] = request.session['signup_key']
    args['site_name'] = settings.SITE_NAME
    
    return render_to_response(template, args)
    
# View for displaying every single product in the DB
def all_products(request):
    result = []
    product_types = ProductType.get_valid()
    
    for product_type in product_types:
        step = []
        c = product_type.get_class()
        step.append(product_type.displayname)
        step.append(c.objects.all())
        result.append(step)

    return append_metadata_to_response(request, 'cotizador/all_products.html',
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
        external_visit.price = store_product.latest_price
        external_visit.save()

    url = store_product.url
    if store_product.store.affiliate_id:
        # Solucion ad-hoc para Peta!
        url += "?a_aid=4ee651f559739"

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        import simplejson
        data = simplejson.dumps({'url': url}, indent=4)
        return HttpResponse(data, mimetype='application/javascript')
    else:
        return HttpResponseRedirect(url)

def sponsored_product_redirect(request, shp_id):
    shp = get_object_or_404(StoreHasProduct, pk = shp_id)
    if not request.user.is_staff:
        sponsored_visit = SponsoredVisit()
        sponsored_visit.shp = shp
        sponsored_visit.save()
    return HttpResponseRedirect(shp.shpe.url)
    
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

@csrf_exempt
def ad_impressed(request):
    ad_id = request.POST['ad_id']
    ad = get_object_or_404(Advertisement, pk=ad_id)

    try:
        aipd = AdvertisementImpressionPerDay.objects.get(
            advertisement=ad,
            date=date.today()
        )
    except AdvertisementImpressionPerDay.DoesNotExist:
        aipd = AdvertisementImpressionPerDay.objects.create(
            advertisement=ad,
            date=date.today(),
            count=0
        )
    aipd.count += 1
    aipd.save()

    return HttpResponse()
    
def product_details_legacy(request, product_id):
    product = get_object_or_404(Product, pk = product_id).get_polymorphic_instance()
    url = reverse('solonotebooks.cotizador.views.product_details', args = [product.url])
    return HttpResponseRedirect(url)
    
# View in charge of showing the details of a product and handle commment submissions        
def product_details(request, product_url):
    match = re.match(r'(\d+)-[\w-]+', product_url)
    product_id = int(match.groups()[0])

    product = get_object_or_404(Product, pk = product_id).get_polymorphic_instance()
    
    if product.url != product_url:
        url = reverse('solonotebooks.cotizador.views.product_details', args = [product.url])
        return HttpResponseRedirect(url)
    
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
        if not request.user.is_staff:
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
        
    template_file = 'templatetags/details_' + product.ptype.adminurlname + '.html'
    
    base_data = {
        'product': product,
        product.ptype.adminurlname: product,
        'comment_form': commentForm,
        'product_prices': stores_with_product_available,
        'product_comments': product.productcomment_set.filter(validated = True).order_by('id'),
        'posted_comment': posted_comment,
        'subscription': product_subscription,
        'ptype': product.ptype
        }
        
    extra_data = product.extra_data(request)
    base_data.update(extra_data)
    
    try:
        return append_metadata_to_response(request, template_file, base_data)
    except:
        return append_metadata_to_response(request, 'templatetags/details_generic.html', base_data)
