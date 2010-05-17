import operator
from django.db.models import Min
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from solonotebooks.cotizador.models import *
from utils import stringCompare
import sys
import cairo
import datetime
from math import ceil
from forms.search_form import SearchForm
from difflib import SequenceMatcher
                    
class NotebookCommentForm(forms.Form):
    comments = forms.CharField(widget = forms.Textarea)
    nickname = forms.CharField(max_length = 255)
    
def store_data(request, store_id):
    store = get_object_or_404(Store, pk = store_id)
    search_form = SearchForm(request.GET)
        
    return render_to_response('cotizador/store_details.html', {
        'form': search_form,
        'store': store,
    })
    
def store_index(request):
    stores = Store.objects.all()
    search_form = SearchForm(request.GET)
    return render_to_response('cotizador/store_index.html', {
        'form': search_form,
        'stores': stores,
    })  
    
def search(request):
    search_form = SearchForm(request.GET)
    query = request.GET['search_keywords']
    
    available_notebooks = Notebook.objects.all().filter(is_available=True).order_by('?')
    
    result_notebooks = [[ntbk, stringCompare(ntbk.rawText(), query)] for ntbk in available_notebooks]
    result_notebooks = filter(lambda(x): x[1] > 10, result_notebooks) 
    result_notebooks = sorted(result_notebooks, key = operator.itemgetter(1), reverse = True)
    
    if 'page_number' in request.GET:
        page_number = int(request.GET['page_number'])
    else:
        page_number = 1
        
    page_count = ceil(len(result_notebooks) / 10.0);
    result_notebooks = result_notebooks[(page_number - 1) * 10 : page_number * 10]
    pages = filter(lambda(x): x > 0 and x <= page_count, range(page_number - 3, page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
    
    
    return render_to_response('cotizador/search.html', {
        'query': query,
        'form': search_form,
        'ntbk_results': result_notebooks,
        'page_number': page_number,
        'prev_page': page_number - 1,
        'post_page': page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,        
    })
    
    
def browse(request):
    search_form = SearchForm(request.GET)
    
    
    if 'advanced_controls' in search_form.data and search_form.data['advanced_controls'] and int(search_form.data['advanced_controls']):
        advanced_controls = True
    else:
        advanced_controls = False
        
    result_notebooks = Notebook.objects.all().filter(is_available=True)
    
    if 'notebook_brand' in search_form.data and search_form.data['notebook_brand']:
        result_notebooks = result_notebooks.filter(line__brand__id=search_form.data['notebook_brand'])
        
    if 'weight' in search_form.data and search_form.data['weight'] and advanced_controls:
        req_weight = int(search_form.data['weight'])
        result_notebooks = result_notebooks.filter(weight__gte = req_weight * 1000)
        result_notebooks = result_notebooks.filter(weight__lte = (req_weight + 1) * 1000)        
        
    if 'processor_brand' in search_form.data and search_form.data['processor_brand']:
        result_notebooks = result_notebooks.filter(processor__line__family__brand__id=search_form.data['processor_brand'])
        
    if 'processor_line_family' in search_form.data and search_form.data['processor_line_family']:
        result_notebooks = result_notebooks.filter(processor__line__family__id=search_form.data['processor_line_family'])
        
    if 'ram_quantity' in search_form.data and search_form.data['ram_quantity']:
        result_notebooks = result_notebooks.filter(ram_quantity__value__gte=RamQuantity.objects.get(pk = search_form.data['ram_quantity']).value)
        
    if 'storage_capacity' in search_form.data and search_form.data['storage_capacity']:
        result_notebooks = result_notebooks.filter(storage_drive__capacity__value__gte = StorageDriveCapacity.objects.get(pk = search_form.data['storage_capacity']).value).distinct()
        
    if 'screen_size_family' in search_form.data and search_form.data['screen_size_family']:
        result_notebooks = result_notebooks.filter(screen__size__family__id = search_form.data['screen_size_family'])
        
    if 'video_card_type' in search_form.data and search_form.data['video_card_type']:
        result_notebooks = result_notebooks.filter(video_card__card_type__id = search_form.data['video_card_type']).distinct()
        
    if 'operating_system' in search_form.data and search_form.data['operating_system']:
        result_notebooks = result_notebooks.filter(operating_system__family__id = search_form.data['operating_system'])
        
    if 'notebook_line' in search_form.data and search_form.data['notebook_line'] and advanced_controls:
        result_notebooks = result_notebooks.filter(line__id=search_form.data['notebook_line'])
        
    if 'processor_line' in search_form.data and search_form.data['processor_line'] and advanced_controls:
        result_notebooks = result_notebooks.filter(processor__line__id=search_form.data['processor_line'])
        
    if 'processor_family' in search_form.data and search_form.data['processor_family'] and advanced_controls:
        result_notebooks = result_notebooks.filter(processor__family__id=search_form.data['processor_family'])
        
    if 'processor' in search_form.data and search_form.data['processor'] and advanced_controls:
        result_notebooks = result_notebooks.filter(processor__id=search_form.data['processor'])
        
    if 'chipset' in search_form.data and search_form.data['chipset'] and advanced_controls:
        result_notebooks = result_notebooks.filter(chipset__id=search_form.data['chipset'])
        
    if 'ram_type' in search_form.data and search_form.data['ram_type'] and advanced_controls:
        result_notebooks = result_notebooks.filter(ram_type__id=search_form.data['ram_type'])
        
    if 'ram_frequency' in search_form.data and search_form.data['ram_frequency'] and advanced_controls:
        result_notebooks = result_notebooks.filter(ram_frequency__value__gte=RamFrequency.objects.get(pk = search_form.data['ram_frequency']).value)
        
    if 'storage_type' in search_form.data and search_form.data['storage_type'] and advanced_controls:
        result_notebooks = result_notebooks.filter(storage_drive__drive_type__id = search_form.data['storage_type'])
        
    if 'screen_size' in search_form.data and search_form.data['screen_size'] and advanced_controls:
        result_notebooks = result_notebooks.filter(screen__size__id = search_form.data['screen_size'])
        
    if 'screen_resolution' in search_form.data and search_form.data['screen_resolution'] and advanced_controls:
        result_notebooks = result_notebooks.filter(screen__resolution__id = search_form.data['screen_resolution'])
        
    if 'screen_touch' in search_form.data and search_form.data['screen_touch'] and advanced_controls:
        result_notebooks = result_notebooks.filter(screen__is_touchscreen = search_form.data['screen_touch'])    
        
    if 'video_card_brand' in search_form.data and search_form.data['video_card_brand'] and advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__line__brand__id = search_form.data['video_card_brand']).distinct()
        
    if 'video_card_line' in search_form.data and search_form.data['video_card_line'] and advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__line__id = search_form.data['video_card_line']).distinct()
        
    if 'video_card' in search_form.data and search_form.data['video_card'] and advanced_controls:
        result_notebooks = result_notebooks.filter(video_card__id = search_form.data['video_card']).distinct()
    
    if 'page_number' in search_form.data:
        page_number = int(search_form.data['page_number'])
    else:
        page_number = 1
        
    page_count = ceil(result_notebooks.count() / 10.0);
    result_notebooks = result_notebooks.order_by('min_price')[(page_number - 1) * 10 : page_number * 10]
    pages = filter(lambda(x): x > 0 and x <= page_count, range(page_number - 3, page_number + 3))
    try:
        left_page = pages[0]
    except:
        left_page = 0
        
    try:
        right_page = pages[len(pages) - 1]
    except:
        right_page = 0
       
    return render_to_response('cotizador/index.html', {
        'form': search_form,
        'remove_filter_links': search_form.generateRemoveFilterLinks(),
        'result_notebooks': result_notebooks,
        'page_number': page_number,
        'prev_page': page_number - 1,
        'post_page': page_number + 1,
        'page_count': int(page_count),
        'page_range': pages,
        'left_page': left_page,
        'right_page': right_page,
    })
    
def all_notebooks(request):
    notebooks = Notebook.objects.all()
    search_form = SearchForm(request.GET)
        
    return render_to_response('cotizador/all_notebooks.html', {
        'form': search_form,
        'result_notebooks': notebooks
    })
    
    
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
        
def notebook_details(request, notebook_id):
    notebook = get_object_or_404(Notebook, pk = notebook_id)
    notebook = Notebook.objects.all().get(pk = notebook_id)
    search_form = SearchForm(request.GET)
    
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
        
    posted_comment = False
    
    if request.user.is_authenticated():
        admin_user = True
    else:
        admin_user = False
    
    if 'posted_comment' in request.session and request.session['posted_comment'] == True:
        posted_comment = True
        request.session['posted_comment'] = False
    
    
    stores_with_notebook_available = notebook.storehasnotebook_set.all().filter(is_available=True)
    price_changes = notebook.notebookpricechange_set.all().order_by('date')
    
    return render_to_response('cotizador/notebook_details.html', {
        'notebook': notebook,
        'form': search_form,
        'comment_form': commentForm,
        'notebook_prices': stores_with_notebook_available,
        'notebook_comments': notebook.notebookcomment_set.filter(validated = True).order_by('date'),
        'posted_comment': posted_comment,
        'admin_user': admin_user,
        'price_changes': price_changes,
        'similar_notebooks': notebook.findSimilarNotebooks(),
        })
        
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
        return render_to_response('cotizador/login.html', {
                'form': SearchForm(),
            })
    
@login_required    
def news(request):
    last_logs = LogEntry.objects.filter(date__gte = datetime.date.today() - datetime.timedelta(days = 7)).order_by('-date').all()
    return render_to_response('cotizador/manager_news.html', {
            'form': SearchForm(),
            'last_logs': last_logs,
        })
        
@login_required    
def comments(request):
    due_comments = NotebookComment.objects.filter(validated = False)
    return render_to_response('cotizador/manager_comments.html', {
            'form': SearchForm(),
            'due_comments': due_comments,
        })
        
@login_required    
def new_notebooks(request):
    new_notebooks = StoreHasNotebook.objects.filter(is_available = True).filter(is_hidden = False).filter(notebook = None)
    return render_to_response('cotizador/manager_new_notebooks.html', {
            'form': SearchForm(),
            'new_notebooks': new_notebooks,
        })
        
@login_required
def hide_notebook(request, store_has_notebook_id):
    shn = get_object_or_404(StoreHasNotebook, pk = store_has_notebook_id)
    shn.is_hidden = True
    shn.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);

@login_required            
def delete_comment(request, comment_id):
    comment = get_object_or_404(NotebookComment, pk = comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);
            
def validate_all(request):
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
            
def processor_line_family_details(request, processor_line_family_id):
    processor_line_family = get_object_or_404(ProcessorLineFamily, pk = processor_line_family_id)
    search_form = SearchForm(request.GET)
    return render_to_response('cotizador/processor_line_family_details.html', {
                'form': search_form,
                'processor_line_family': processor_line_family
            })
