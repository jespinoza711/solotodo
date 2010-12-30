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
    # Initialize the "form" that defines what special notebooks to 
    # display (by New, Price or Popularity) and get the corresponding
    # notebooks
    highlighted_notebooks_form = HighlightedNotebooksForm.initialize(request.GET)
    result_notebooks = highlighted_notebooks_form.apply_filter(Notebook.get_valid())[:10]
    
    return append_ads_to_response(request, 'cotizador/index.html', {
        'hnf': highlighted_notebooks_form,
        'notebooks': result_notebooks
    })    
    
# View that handles the main catalog, applying filters and ordering
# (/catalog)
def catalog(request):
    search_form = initialize_search_form(request.GET)
    search_form.save()
    
    # Grab all the candidates (those currently available)
    result_notebooks, ordering_direction = filter_notebooks(Notebook.get_valid(), search_form)
    num_results = len(result_notebooks)
    
    page_count = ceil(len(result_notebooks) / 10.0);        
    
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
    result_notebooks = result_notebooks[first_result_index - 1 : last_result_index]
    
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
    d = dict(SearchForm.price_choices)
    
    return append_ads_to_response(request, 'cotizador/catalog.html', {
        'form': search_form,
        'max_price': d[str(search_form.max_price)], 
        'min_price': d[str(search_form.min_price)],
        'remove_filter_links': search_form.generate_remove_filter_links(),
        'change_ntype_url': search_form.generate_url_without_ntype(),
        'num_results': num_results,
        'first_result_index': first_result_index,
        'last_result_index': last_result_index,
        'notebooks': result_notebooks,
        'current_url': search_form.generateUrlWithoutOrdering(),
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'left_page': left_page,
        'right_page': right_page,
        'page_range': pages,
        'ordering': str(search_form.ordering),
    })
    
# View in charge of showing the details of a notebook and handle commment submissions        
def notebook_details(request, notebook_id):
    notebook = get_object_or_404(Notebook, pk = notebook_id)
    notebook = Notebook.objects.all().get(pk = notebook_id)
    
    # If this is a comment submission, validate and save
    if request.method == 'POST': 
        commentForm = NotebookCommentForm(request.POST)
        if commentForm.is_valid():
            notebook_comment = NotebookComment()
            notebook_comment.date = date.today()        
            rawComment = commentForm.cleaned_data['comments']
            notebook_comment.comments = rawComment.replace('\n', '<br />')
            notebook_comment.notebook = notebook
            if not request.user.is_anonymous():
                notebook_comment.user = request.user
                notebook_comment.validated = True
            else:
                notebook_comment.nickname = commentForm.cleaned_data['nickname']
                request.session['posted_comment'] = True
                
            notebook_comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER']);
    else:
        commentForm = NotebookCommentForm()
        
        
    # Check if this is the redirect response generated after submitting an anonymous comment
    # If it is, show a message that the comment needs to be validated and hide
    # the form (to prevent users from posting again feeling that it didn't work)
    posted_comment = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    # Find the stores with this notebook available
    stores_with_notebook_available = notebook.storehasnotebook_set.all().filter(is_available=True).filter(is_hidden = False).order_by('latest_price')
        
    max_suggested_price = int(notebook.min_price * 1.10 / 1000) * 1000
    similar_notebooks_ids = notebook.similar_notebooks.split(',')
    similar_notebooks = [Notebook.objects.get(pk = ntbk_id) for ntbk_id in similar_notebooks_ids if ntbk_id]
    
    try:
        notebook_subscription = NotebookSubscription.objects.filter(user = request.user, notebook = notebook, is_active = True)[0]
    except:
        notebook_subscription = None
    
    return append_ads_to_response(request, 'cotizador/notebook_details.html', {
        'notebook': notebook,
        'comment_form': commentForm,
        'notebook_prices': stores_with_notebook_available,
        'notebook_comments': notebook.notebookcomment_set.filter(validated = True).order_by('date'),
        'posted_comment': posted_comment,
        'similar_notebooks': similar_notebooks,
        'notebook_subscription': notebook_subscription,
        })    
    
def latest_notebooks(request):
    ntbks = Notebook.objects.filter(is_available = True).order_by('-date_added')[:10]
    
    response = dict([[str(ntbk.id), str(ntbk)] for ntbk in ntbks])
        
    data = simplejson.dumps(response, indent=4)    
    return HttpResponse(data, mimetype='application/javascript')     
    
# View for showing a particular store with the notebooks it offers    
def store_details(request, store_id):
    store = get_object_or_404(Store, pk = store_id)
    shns = StoreHasNotebook.objects.filter(store = store).filter(~Q(notebook = None)).filter(is_available = True).order_by('latest_price')
        
    return append_ads_to_response(request, 'cotizador/store_details.html', {
        'store': store,
        'shns': shns,
    })
    
# View for showing all of the stores currently in the DB    
def store_index(request):
    stores = Store.objects.all()
    return append_ads_to_response(request, 'cotizador/store_index.html', {
        'stores': stores,
    })  
    
# View for handling the search of notebooks using keywords    
def search(request):
    # The keywords
    try:
        query = request.GET['search_keywords']
        if not query:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')
    
    # We grab all the candidates (those currently available)
    available_notebooks = Notebook.get_valid()
    
    # For each one, we assign a score base on how many of the keywords match a 
    # huge single line description of the notebook stored in the DB
    result_notebooks = [[ntbk, stringCompare(ntbk.long_description, query)] for ntbk in available_notebooks]
    # If the hit is too low (< 10%) they are eliminated
    result_notebooks = filter(lambda(x): x[1] > 10, result_notebooks) 
    # Finally we sort them from highest to lowest hit rate
    result_notebooks = sorted(result_notebooks, key = operator.itemgetter(1), reverse = True)
    
    # Boilerplate code for setting up the links to each page of the results
    search_form = initialize_search_form(request.GET)
    
    page_count = ceil(len(result_notebooks) / 10.0);
        
    pages = filter(lambda(x): x > 0 and x <= page_count, range(search_form.page_number - 3, search_form.page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
        
    result_notebooks = result_notebooks[(search_form.page_number - 1) * 10 : search_form.page_number * 10]
    
    for result in result_notebooks:
        result[0].matching = result[1]
        
    result_notebooks = [result[0] for result in result_notebooks]
    
    return append_ads_to_response(request, 'cotizador/search.html', {
        'form': search_form,
        'query': query,
        'ntbk_results': result_notebooks,
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,        
    })
    
def append_ads_to_response(request, template, args):
    args['side_ad'] = load_advertisement('Side')
    args['top_ad'] = load_advertisement('Top')
    
    return append_user_to_response(request, template, args)
    
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
        
    ntype_comparison_key = str(args['form'].ntype)
    if ntype_comparison_key == '0':
        ntype_comparison_key = '';
    
    args['ntype_comparison_key'] = ntype_comparison_key
    args['signup_key'] = request.session['signup_key']
    return render_to_response(template, args)
       
    return append_ads_to_response(request, 'cotizador/index.html', {
        'form': search_form,
        'remove_filter_links': search_form.generateRemoveFilterLinks(),
        'result_notebooks': result_notebooks,
        'produt_link_args': product_link_args,
        'ordering_direction_url': search_form.generateUrlWithoutOrderingDirection(),
        'ordering_direction': {'': 0, '-': 1}[ordering_direction],
    })
    
# View for displaying every single notebook in the DB
def all_notebooks(request):
    notebooks = Notebook.objects.all()
    
    return append_ads_to_response(request, 'cotizador/all_notebooks.html', {
        'result_notebooks': notebooks
    })
    
# View that gets called when a user clicks an external link to a store
# we log this for statistical purposes and... maybe build a business model
# someday...
def store_notebook_redirect(request, store_notebook_id):
    store_notebook = get_object_or_404(StoreHasNotebook, pk = store_notebook_id)
    store_notebook.save()
    external_visit = ExternalVisit()
    external_visit.shn = store_notebook
    external_visit.date = date.today()
    external_visit.save()
    return HttpResponseRedirect(store_notebook.url)
    
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
        
# View in charge of showing the details of a notebook and handle commment submissions        
def notebook_details(request, notebook_id):
    notebook = get_object_or_404(Notebook, pk = notebook_id)
    notebook = Notebook.objects.all().get(pk = notebook_id)
    
    # If this is a comment submission, validate and save
    if request.method == 'POST': 
        commentForm = NotebookCommentForm(request.POST)
        if commentForm.is_valid():
            notebook_comment = NotebookComment()
            notebook_comment.date = date.today()        
            rawComment = commentForm.cleaned_data['comments']
            notebook_comment.comments = rawComment.replace('\n', '<br />')
            notebook_comment.notebook = notebook
            if not request.user.is_anonymous():
                notebook_comment.user = request.user
                notebook_comment.validated = True
            else:
                notebook_comment.nickname = commentForm.cleaned_data['nickname']
                request.session['posted_comment'] = True
                
            notebook_comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER']);
    else:
        commentForm = NotebookCommentForm()
        
        
    # Check if this is the redirect response generated after submitting an anonymous comment
    # If it is, show a message that the comment needs to be validated and hide
    # the form (to prevent users from posting again feeling that it didn't work)
    posted_comment = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    # Find the stores with this notebook available
    stores_with_notebook_available = notebook.storehasnotebook_set.all().filter(is_available=True).filter(is_hidden = False).order_by('latest_price')
        
    max_suggested_price = int(notebook.min_price * 1.10 / 1000) * 1000
    similar_notebooks_ids = notebook.similar_notebooks.split(',')
    similar_notebooks = [Notebook.objects.get(pk = ntbk_id) for ntbk_id in similar_notebooks_ids if ntbk_id]
    
    try:
        notebook_subscription = NotebookSubscription.objects.filter(user = request.user, notebook = notebook, is_active = True)[0]
    except:
        notebook_subscription = None
    
    return append_ads_to_response(request, 'cotizador/notebook_details.html', {
        'notebook': notebook,
        'comment_form': commentForm,
        'notebook_prices': stores_with_notebook_available,
        'notebook_comments': notebook.notebookcomment_set.filter(validated = True).order_by('id'),
        'posted_comment': posted_comment,
        'similar_notebooks': similar_notebooks,
        'notebook_subscription': notebook_subscription,
        })
            
# View in charge of showing the processors of a particular line, nothing fancy            
def redirect_processor_line_family_details(request, processor_line_family_id):
    url = reverse('solonotebooks.cotizador.views.processor_line_details', args = [processor_line_family_id])
    url += concat_dictionary(request.GET)
    return HttpResponseRedirect(url)
            
def processor_line_details(request, processor_line_id):
    processor_line_family = get_object_or_404(ProcessorLineFamily, pk = processor_line_id)
    other_processor_line_families = ProcessorLineFamily.objects.filter(~Q(id = processor_line_family.id))
    
    processor_id = 0
    if 'processor' in request.GET:
        try:
            processor_id = int(request.GET['processor'])
        except:
            processor_id = 0
            
        try:
            processor = Processor.objects.filter(line__family = processor_line_family).get(pk = processor_id)
            ntbks = Notebook.get_valid().filter(processor = processor).order_by('?')[0:5]
        except:
            processor = None
            ntbks = Notebook.get_valid().filter(processor__line__family = processor_line_family).order_by('?')[0:5]
    else:
        processor = None
        ntbks = Notebook.get_valid().filter(processor__line__family = processor_line_family).order_by('?')[0:5]
        
    processors = Processor.objects.filter(line__family = processor_line_family).order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/processor_line_details.html', {
                'processor_line_family': processor_line_family,
                'processors': processors,
                'ntbks': ntbks,
                'processor_id': processor_id,
                'processor': processor,
                'other_processor_line_families': other_processor_line_families,
            })
            
def video_card_line_details(request, video_card_line_id):
    video_card_line = get_object_or_404(VideoCardLine, pk = video_card_line_id)
    other_video_card_lines = VideoCardLine.objects.filter(~Q(id = video_card_line.id))
    video_card_id = 0
    if 'video_card' in request.GET:
        try:
            video_card_id = int(request.GET['video_card'])
        except: 
            video_card_id = 0
            
        try:
            video_card = VideoCard.objects.filter(line = video_card_line).get(pk = video_card_id)
            ntbks = Notebook.get_valid().filter(video_card = video_card).order_by('?').distinct()[0:5]
        except:
            video_card = None
            ntbks = Notebook.get_valid().filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    else:
        video_card = None    
        ntbks = Notebook.get_valid().filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    
    video_cards = VideoCard.objects.filter(line = video_card_line).order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/video_card_line_details.html', {
                'video_card_line': video_card_line,
                'video_cards': video_cards,
                'ntbks': ntbks,
                'video_card_id': video_card_id,
                'video_card': video_card,
                'other_video_card_lines': other_video_card_lines,
            })            
            
def redirect_all_processor_line_families(request):
    url = reverse('solonotebooks.cotizador.views.processor_line')
    return HttpResponseRedirect(url)
            
def processor_line(request):
    processor_line_families = ProcessorLineFamily.objects.all()
    processors = Processor.objects.order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/all_processor_lines.html', {
        'processor_line_families': processor_line_families,
        'processors': processors
    })            
            
def video_card_line(request):
    video_card_lines = VideoCardLine.objects.all()
    video_cards = VideoCard.objects.order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/all_video_card_lines.html', {
                'video_card_lines': video_card_lines,
                'video_cards': video_cards
            })
