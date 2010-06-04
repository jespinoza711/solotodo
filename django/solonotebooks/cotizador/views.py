import operator
from django.db.models import Min, Max, Q
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from utils import stringCompare
import sys
import cairo
import datetime
from math import ceil
from forms.search_form import SearchForm
from difflib import SequenceMatcher
import pdb
                   
# Class that represents the form in which the users can leave comments for a notebook                    
class NotebookCommentForm(forms.Form):
    comments = forms.CharField(widget = forms.Textarea)
    nickname = forms.CharField(max_length = 255)
    
# View for showing a particular store with the notebooks it offers    
def store_data(request, store_id):
    store = get_object_or_404(Store, pk = store_id)
    search_form = initialize_search_form(request.GET)
    shns = StoreHasNotebook.objects.filter(store = store).filter(~Q(notebook = None)).order_by('latest_price')
        
    return render_to_response('cotizador/store_details.html', {
        'form': search_form,
        'store': store,
        'shns': shns,
    })
    
# View for showing all of the stores currently in the DB    
def store_index(request):
    stores = Store.objects.all()
    search_form = initialize_search_form(request.GET)
    return render_to_response('cotizador/store_index.html', {
        'form': search_form,
        'stores': stores,
    })  
    
# View for handling the search of notebooks using keywords    
def search(request):
    search_form = initialize_search_form(request.GET)
    
    # The keywords
    query = request.GET['search_keywords']
    
    # We grab all the candidates (those currently available)
    available_notebooks = Notebook.objects.all().filter(is_available=True)
    
    # For each one, we assign a score base on how many of the keywords match a 
    # huge single line description of the notebook stored in the DB
    result_notebooks = [[ntbk, stringCompare(ntbk.long_description, query)] for ntbk in available_notebooks]
    # If the hit is too low (< 10%) they are eliminated
    result_notebooks = filter(lambda(x): x[1] > 10, result_notebooks) 
    # Finally we sort them from highest to lowest hit rate
    result_notebooks = sorted(result_notebooks, key = operator.itemgetter(1), reverse = True)
    
    # Boilerplate code for setting up the links to each page of the results
    
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
    
    
    
    return render_to_response('cotizador/search.html', {
        'query': query,
        'form': search_form,
        'ntbk_results': result_notebooks,
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,        
    })
    
# View that handles the main search / browse windows, applying filters and ordering    
def browse(request):
    search_form = initialize_search_form(request.GET)
        
    # Grab all the candidates (those currently available)
    result_notebooks = Notebook.objects.all().filter(is_available=True)
    
    # And apply each active filter...
    if search_form.notebook_brand:
        result_notebooks = result_notebooks.filter(line__brand__id = search_form.notebook_brand)
        
    if search_form.weight and search_form.advanced_controls:
        req_weight = search_form.weight;
        result_notebooks = result_notebooks.filter(weight__gte = (req_weight - 1) * 1000)
        result_notebooks = result_notebooks.filter(weight__lte = req_weight * 1000)        
        
    if search_form.processor_brand:
        result_notebooks = result_notebooks.filter(processor__line__family__brand__id = search_form.processor_brand)
        
    if search_form.processor_line_family:
        result_notebooks = result_notebooks.filter(processor__line__family__id = search_form.processor_line_family)
        
    if search_form.ram_quantity:
        result_notebooks = result_notebooks.filter(ram_quantity__value__gte = RamQuantity.objects.get(pk = search_form.ram_quantity).value)
        
    if search_form.storage_capacity:
        result_notebooks = result_notebooks.filter(storage_drive__capacity__value__gte = StorageDriveCapacity.objects.get(pk = search_form.storage_capacity).value).distinct()
        
    if search_form.screen_size_family:
        result_notebooks = result_notebooks.filter(screen__size__family__id = search_form.screen_size_family)
        
    if search_form.video_card_type:
        result_notebooks = result_notebooks.filter(video_card__card_type__id = search_form.video_card_type).distinct()
        
    if search_form.operating_system:
        result_notebooks = result_notebooks.filter(operating_system__family__id = search_form.operating_system)
        
    if search_form.notebook_line and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(line__id=search_form.notebook_line)
        
    if search_form.processor_line and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(processor__line__id=search_form.processor_line)
        
    if search_form.processor_family and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(processor__family__id=search_form.processor_family)
        
    if search_form.processor and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(processor__id=search_form.processor)
        
    if search_form.chipset and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(chipset__id=search_form.chipset)
        
    if search_form.ram_type and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(ram_type__id=search_form.ram_type)
        
    if search_form.ram_frequency and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(ram_frequency__value__gte=RamFrequency.objects.get(pk = search_form.ram_frequency).value)
        
    if search_form.storage_type and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(storage_drive__drive_type__id = search_form.storage_type)
        
    if search_form.screen_size and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(screen__size__id = search_form.screen_size)
        
    if search_form.screen_resolution and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(screen__resolution__id = search_form.screen_resolution)
        
    if search_form.screen_touch and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(screen__is_touchscreen = search_form.screen_touch)    
        
    if search_form.video_card_brand and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__line__brand__id = search_form.video_card_brand).distinct()
        
    if search_form.video_card_line and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__line__id = search_form.video_card_line).distinct()
        
    if search_form.video_card and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__id = search_form.video_card).distinct()
        
    if search_form.min_price and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(min_price__gte = int(search_form.min_price))

    if search_form.max_price and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(min_price__lte = int(search_form.max_price))
        
    # Check the ordering orientation, if it is not set, each criteria uses 
    # sensible defaults (asc fro price, desc for cpu performance, etc)
    ordering_direction = [None, '', '-'][search_form.ordering_direction]
    
    # Apply the corresponding ordering based on the key
    if search_form.ordering == 1:
        if ordering_direction == None:
            ordering_direction = ''
        result_notebooks = result_notebooks.order_by(ordering_direction + 'min_price')
    elif search_form.ordering == 2:
        if ordering_direction == None:
            ordering_direction = '-'    
        result_notebooks = result_notebooks.order_by(ordering_direction + 'processor__speed_score')
    elif search_form.ordering == 3:
        if ordering_direction == None:
            ordering_direction = '-'    
        # Note: A notebook may have more than one video card, grab the fastest
        result_notebooks = result_notebooks.annotate(max_video_card_score=Max('video_card__speed_score')).order_by(ordering_direction + 'max_video_card_score')
    elif search_form.ordering == 4:
        if ordering_direction == None:
            ordering_direction = '-'    
        result_notebooks = result_notebooks.order_by(ordering_direction + 'ram_quantity__value')
    elif search_form.ordering == 5:
        if ordering_direction == None:
            ordering_direction = '-'    
        # Note: A notebook may have more than one SD, grab the biggest
        result_notebooks = result_notebooks.annotate(max_hard_drive_capacity=Max('storage_drive__capacity__value')).order_by(ordering_direction + 'max_hard_drive_capacity')        
    elif search_form.ordering == 6:
        if ordering_direction == None:
            ordering_direction = ''    
        result_notebooks = result_notebooks.order_by(ordering_direction + 'weight')
    else:
        if ordering_direction == None:
            ordering_direction = '-'    
        result_notebooks = result_notebooks.order_by(ordering_direction + 'date_added')
        
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
       
    return render_to_response('cotizador/index.html', {
        'form': search_form,
        'remove_filter_links': search_form.generateRemoveFilterLinks(),
        'result_notebooks': result_notebooks,
        'page_number': search_form.page_number,
        'prev_page': search_form.page_number - 1,
        'post_page': search_form.page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,
        'current_url': search_form.generateUrlWithoutOrdering(),
        'produt_link_args': search_form.generateProdutLinkArgs(),
        'ordering_direction_url': search_form.generateUrlWithoutOrderingDirection(),
        'ordering_direction': {'': 0, '-': 1}[ordering_direction],
        'ordering': str(search_form.ordering),
    })
    
# View for displaying every single notebook in the DB
def all_notebooks(request):
    notebooks = Notebook.objects.all()
    search_form = initialize_search_form(request.GET)
        
    return render_to_response('cotizador/all_notebooks.html', {
        'form': search_form,
        'result_notebooks': notebooks
    })
    
# View that gets called when a user clicks an external link to a store
# we log this for statistical purposes and... maybe build a business model
# someday...
def store_notebook_redirect(request, store_notebook_id):
    store_notebook = get_object_or_404(StoreHasNotebook, pk = store_notebook_id)
    store_notebook.visitorCount += 1
    store_notebook.save()
    external_visit = ExternalVisit()
    external_visit.shn = store_notebook
    external_visit.ip_address = request.META['REMOTE_ADDR']
    external_visit.date = datetime.date.today()
    external_visit.save()
    return HttpResponseRedirect(store_notebook.url)
        
# View in charge of showing the details of a notebook and handle commment submissions        
def notebook_details(request, notebook_id):
    notebook = get_object_or_404(Notebook, pk = notebook_id)
    notebook = Notebook.objects.all().get(pk = notebook_id)
    search_form = initialize_search_form(request.GET)
    
    # If this is a comment submission, validate and save
    if request.method == 'POST': 
        commentForm = NotebookCommentForm(request.POST)
        if commentForm.is_valid():
            notebook_comment = NotebookComment()
            notebook_comment.ip_address = request.META['REMOTE_ADDR']
            notebook_comment.date = datetime.date.today()        
            rawComment = commentForm.cleaned_data['comments']
            notebook_comment.comments = rawComment.replace('\r', '<br />').replace('\n', '<br />')
            notebook_comment.nickname = commentForm.cleaned_data['nickname']
            notebook_comment.notebook = notebook
            notebook_comment.save()
            request.session['posted_comment'] = True
            return HttpResponseRedirect(request.META['HTTP_REFERER']);
    else:
        commentForm = NotebookCommentForm()
        
    # Check if this is the redirect response generated after submitting a comment
    # If it is, show a message that the comment needs to be validated and hide
    # the form (to prevent users from posting again feeling that it didn't work)
    posted_comment = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    # Find the stores with this notebook available
    stores_with_notebook_available = notebook.storehasnotebook_set.all().filter(is_available=True).filter(is_hidden = False).order_by('latest_price')
    
    # If the user is admin, there are some link to allow the editing of the ntbk
    if request.user.is_authenticated():
        admin_user = True
    else:
        admin_user = False
        
    max_suggested_price = int(notebook.min_price * 1.10 / 1000) * 1000
    
    return render_to_response('cotizador/notebook_details.html', {
        'notebook': notebook,
        'form': search_form,
        'comment_form': commentForm,
        'notebook_prices': stores_with_notebook_available,
        'notebook_comments': notebook.notebookcomment_set.filter(validated = True).order_by('date'),
        'posted_comment': posted_comment,
        'admin_user': admin_user,
        'similar_notebooks': notebook.findSimilarNotebooks(),
        'max_suggested_price': max_suggested_price
        })
        
# Page to login to the manager, everything is boilerplate
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        
        if user is not None and user.is_active:
            login(request, user)
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/manager/news/')
    else:
        search_form = initialize_search_form(request.GET)
        return render_to_response('cotizador/login.html', {
                'form': search_form,
            })
    
@login_required    
def news(request):
    # Shows the logs for the last week
    last_logs = LogEntry.objects.filter(date__gte = datetime.date.today() - datetime.timedelta(days = 7)).order_by('-date').all()
    return render_to_response('cotizador/manager_news.html', {
            'form': SearchForm(),
            'last_logs': last_logs,
        })
        
@login_required    
def comments(request):
    # Shows the comments pending for aproval
    due_comments = NotebookComment.objects.filter(validated = False)
    return render_to_response('cotizador/manager_comments.html', {
            'form': SearchForm(),
            'due_comments': due_comments,
        })
        
@login_required    
def new_notebooks(request):
    # Shows the models that don't have an associated notebook in the DB (i.e.: pending)
    new_notebooks = StoreHasNotebook.objects.filter(is_available = True).filter(is_hidden = False).filter(notebook = None)
    return render_to_response('cotizador/manager_new_notebooks.html', {
            'form': SearchForm(),
            'new_notebooks': new_notebooks,
        })
        
@login_required
def hide_notebook(request, store_has_notebook_id):
    # Makes a model invisible to the "pending" page if it is stupid (e.g. iPad)
    # or doesn't apply (combos of notebooks + printers, notebook sleeves, etc)
    shn = get_object_or_404(StoreHasNotebook, pk = store_has_notebook_id)
    shn.is_hidden = True
    shn.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);

@login_required            
def delete_comment(request, comment_id):
    # Deletes a comment
    comment = get_object_or_404(NotebookComment, pk = comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);
            
def validate_all(request):
    # Validates all comments pending approval
    if request.user.is_authenticated():
        comments = NotebookComment.objects.filter(validated = False)
        for comment in comments:
            comment.validated = True
            comment.save()
        return HttpResponseRedirect('/manager')
    else:
        return render_to_response('cotizador/login.html', {
                'form': SearchForm(),
            })
            
# View in charge of showing the processors of a particular line, nothing fancy            
def processor_line_family_details(request, processor_line_family_id):
    processor_line_family = get_object_or_404(ProcessorLineFamily, pk = processor_line_family_id)
    other_processor_line_families = ProcessorLineFamily.objects.filter(~Q(id = processor_line_family.id))
    
    processor_id = 0
    if 'processor' in request.GET:
        try:
            processor_id = int(request.GET['processor'])
        except:
            processor_id = 0
            
        try:
            processor = Processor.objects.filter(line__family = processor_line_family).get(pk = processor_id)
            ntbks = Notebook.objects.filter(processor = processor).order_by('?')[0:5]
        except:
            processor = None
            ntbks = Notebook.objects.filter(processor__line__family = processor_line_family).order_by('?')[0:5]
    else:
        processor = None
        ntbks = Notebook.objects.filter(processor__line__family = processor_line_family).order_by('?')[0:5]
        
    search_form = initialize_search_form(request.GET)
    processors = Processor.objects.filter(line__family = processor_line_family).order_by('-speed_score')
    return render_to_response('cotizador/processor_line_family_details.html', {
                'form': search_form,
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
            ntbks = Notebook.objects.filter(video_card = video_card).order_by('?').distinct()[0:5]
        except:
            video_card = None
            ntbks = Notebook.objects.filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    else:
        video_card = None    
        ntbks = Notebook.objects.filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    search_form = initialize_search_form(request.GET)
    
    video_cards = VideoCard.objects.filter(line = video_card_line).order_by('-speed_score')
    return render_to_response('cotizador/video_card_line_details.html', {
                'form': search_form,
                'video_card_line': video_card_line,
                'video_cards': video_cards,
                'ntbks': ntbks,
                'video_card_id': video_card_id,
                'video_card': video_card,
                'other_video_card_lines': other_video_card_lines,
            })            
            
def all_processor_line_families(request):
    processor_line_families = ProcessorLineFamily.objects.all()
    processors = Processor.objects.order_by('-speed_score')
    search_form = initialize_search_form(request.GET)
    return render_to_response('cotizador/all_processor_line_families.html', {
                'form': search_form,
                'processor_line_families': processor_line_families,
                'processors': processors
            })            
            
def all_video_card_lines(request):
    video_card_lines = VideoCardLine.objects.all()
    video_cards = VideoCard.objects.order_by('-speed_score')
    search_form = initialize_search_form(request.GET)
    return render_to_response('cotizador/all_video_card_lines.html', {
                'form': search_form,
                'video_card_lines': video_card_lines,
                'video_cards': video_cards
            })
            
# Helper method to set the search_form for almost all of the views            
def initialize_search_form(data):
    search_form = SearchForm(data)
    search_form.validate()
    search_form.is_valid()
    
    return search_form
