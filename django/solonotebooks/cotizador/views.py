#-*- coding: UTF-8 -*-
import os
import sys
import hashlib
import cairo
import operator
from datetime import date, timedelta
from time import time
from math import ceil
from pycha.pie import PieChart
from django.db.models import Min, Max, Q
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

def manager_login_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect('/account/login')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
def latest_notebooks(request):
    ntbks = Notebook.objects.filter(is_available = True).order_by('-date_added')[:10]
    
    response = dict([[str(ntbk.id), str(ntbk)] for ntbk in ntbks])
        
    data = simplejson.dumps(response, indent=4)    
    return HttpResponse(data, mimetype='application/javascript')     
    
# View for showing a particular store with the notebooks it offers    
def store_data(request, store_id):
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
    available_notebooks = Notebook.objects.all().filter(is_available=True)
    
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
    args['user'] = request.user
    args['flash'] = request.flash
    if 'REQUEST_URI' in request.META:
            args['next'] = urlquote(request.META['REQUEST_URI'])
    if 'signup_key' not in request.session:
        request.session['signup_key'] = int(time())
        
    if 'form' not in args:
        args['form'] = initialize_search_form(request.GET)
    args['signup_key'] = request.session['signup_key']
    return render_to_response(template, args)    
    
# View that handles the main search / browse windows, applying filters and ordering    
def browse(request):
    search_form = initialize_search_form(request.GET)
    search_form.save()
        
    # Grab all the candidates (those currently available)
    result_notebooks = Notebook.objects.all().filter(is_available=True)
    
    # And apply each active filter...
    if search_form.usage:
        value = search_form.usage
        if value == 1:
            result_notebooks = result_notebooks.filter(screen__size__family__base_size__gte = 13).filter(screen__size__family__base_size__lt = 16).filter(ram_quantity__value__gte = 2).filter(processor__speed_score__gte = 900).filter(storage_drive__capacity__value__gte = 160).distinct()
        elif value == 2:
            result_notebooks = result_notebooks.filter(screen__size__family__base_size__gte = 7).filter(screen__size__family__base_size__lt = 12).filter(Q(processor__line__family__id = 11)|Q(processor__line__family__id = 1))
        elif value == 3:
            result_notebooks = result_notebooks.filter(screen__size__family__base_size__gte = 11).filter(screen__size__family__base_size__lt = 13).filter(processor__line__family__id = 2)
        elif value == 4:
            result_notebooks = result_notebooks.filter(ram_quantity__value__gte = 2).filter(processor__speed_score__gte = 1300).filter(video_card__speed_score__gte = 3000).filter(storage_drive__capacity__value__gte = 250).distinct()
    
    if search_form.notebook_brand:
        result_notebooks = result_notebooks.filter(line__brand__id = search_form.notebook_brand)
        
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
        
    if search_form.processor and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(processor__id=search_form.processor)
        
    if search_form.ram_type and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(ram_type__id=search_form.ram_type)
        
    if search_form.storage_type and search_form.advanced_controls:
        result_notebooks = result_notebooks.filter(storage_drive__drive_type__id = search_form.storage_type)
        
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
        
    if search_form.min_price:
        result_notebooks = result_notebooks.filter(min_price__gte = int(search_form.min_price))

    if search_form.max_price:
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
       
    return append_ads_to_response(request, 'cotizador/index.html', {
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
    
    return append_ads_to_response(request, 'cotizador/all_notebooks.html', {
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
    external_visit.ip_address = ''
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
        
# Page to login to the account, everything is boilerplate
def login(request):
    next_url = '/'
    if 'next' in request.GET:
        next_url = request.GET['next']
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
        else:
            request.flash['error'] = 'Nombre de usuario o contraseña incorrectos'
            return HttpResponseRedirect('/account/login/?next=%s' % urlquote(next_url))
    
    if request.user.is_authenticated():
        return HttpResponseRedirect(next_url)
    else:
        return append_ads_to_response(request, 'cotizador/login.html', {
            })
            
def ajax_login(request):
    response = {'code': 'ERROR'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            response['code'] = 'OK'
            response['message'] = 'OK'
        else:
            response['message'] = 'Nombre de usuario o contraseña incorrectos'
    else:
        response['message'] = 'Error en el proceso de login'
        
    data = simplejson.dumps(response, indent=4)    
    return HttpResponse(data, mimetype='application/javascript') 
            
@login_required    
def logout(request):
    auth.logout(request)
    next_url = '/'
    if 'next' in request.GET:
        next_url = request.GET['next']
    return HttpResponseRedirect(next_url)
        
    
def signup(request):
    response = {'code': 'ERROR'}
    if request.method == 'POST':
        try:
            username = request.POST['username']
            if username == '':
                raise FormException('Debe introducir un nombre de usuario')
            if len(username) > 30:
                raise FormException('El nombre de usuario debe tener menos de 30 caracteres')
            
            existing_users = User.objects.filter(username = username)
            if existing_users:
                raise FormException('El nombre de usuario ya esta tomado')
                
            email = request.POST['email']
            if not email_re.match(email):
                raise FormException('Por favor ingrese un correo electrónico válido')
                
            password = request.POST['password']
            if password == '':
                raise FormException('Debe ingresar una contraseña')
            
            repeat_password = request.POST['repeat_password']
            if repeat_password != password:
                raise FormException('Las contraseñas no concuerdan')
            
            signup_key = int(request.POST['signup_key'])
            if signup_key != request.session['signup_key']:
                raise FormException('Error desconocido')                
            
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()
            
            auth_user = auth.authenticate(username = username, password = password)
            auth.login(request, auth_user)
            
            send_signup_mail(user)
            
            response['code'] = 'OK'
            response['message'] = 'OK'
            
        except FormException, e:
            response['message'] = str(e)
        except Exception, e:
            if user:
                user.delete()
            response['message'] = 'Error desconocido'
    else:
        response['message'] = 'Error desconocido'

    data = simplejson.dumps(response, indent=4)    
    return HttpResponse(data, mimetype='application/javascript')

@login_required    
def add_subscription(request):
    try:
        notebook = Notebook.objects.get(pk = request.GET['notebook'])
        user = request.user
        
        existing_notebook_subscriptions = NotebookSubscription.objects.filter(user = user).filter(notebook = notebook)
        if existing_notebook_subscriptions:
            notebook_subscription = existing_notebook_subscriptions[0]
            notebook_subscription.is_active = True
        else:
            notebook_subscription = NotebookSubscription()
            notebook_subscription.user = user
            notebook_subscription.notebook = notebook                                
            
        notebook_subscription.email_notifications = bool(int(request.GET['email_notifications']))
        notebook_subscription.save()
        
        request.flash['message'] = 'Suscripción agregada'
    except Exception, e:
        request.flash['error'] = 'Error desconocido'

    return HttpResponseRedirect('/notebooks/%d' % notebook.id )    
    
@login_required
def validate_email(request):
    try:
        user = request.user
        if user.is_active:
            raise MailValidationException('El correo ya está validado')
        validation_key = request.GET['validation_key']
        orig_validation_key = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()
        if validation_key != orig_validation_key:
            raise MailValidationException('Error en código de validación')
            
        user.is_active = True;
        user.get_profile().change_mails_sent = 0;
        user.get_profile().confirmation_mails_sent = 0;
        user.get_profile().save()
        
        user.save()
        request.flash['message'] = 'Cuenta de correo activada correctamente'
        return HttpResponseRedirect('/account/')        
    except MailValidationException, e:
        error = str(e)
    except Exception, e:
        error = 'Error desconocido'
    return append_ads_to_response(request, 'account/validate_email.html', {
            'error': error,
        })

def request_password_regeneration(request):
    response = {'code': 'ERROR'}
    if request.method == 'POST':
        try:
            username = request.POST['username']
            if username == '':
                raise FormException('Debe introducir un nombre de usuario')
            
            existing_users = User.objects.filter(username = username)
            if not existing_users:
                raise FormException('El usuario no existe')
            
            user = existing_users[0]
            
            if not user.is_active:
                raise FormException('El correo del usuario no ha sido validado')
            
            send_password_regeneration_mail(user)
            
            response['code'] = 'OK'
            response['message'] = 'OK'
            
        except FormException, e:
            response['message'] = str(e)
        except MailException, e:
            response['message'] = str(e)
        except Exception, e:
            response['message'] = 'Error desconocido'
    else:
        response['message'] = 'Error desconocido'

    data = simplejson.dumps(response, indent=4)    
    return HttpResponse(data, mimetype='application/javascript')
    
def regenerate_password(request):
    try:
        user_id = int(request.GET['id'])
        validation_key = request.GET['validation_key']
        user = User.objects.get(pk = user_id)
        
        orig_validation_key = hashlib.sha224(settings.SECRET_KEY + user.username + user.password).hexdigest()
        if validation_key != orig_validation_key:
            raise PasswordRegenerationException('Error en llave de validación')
            
        new_password = User.objects.make_random_password()
        
        send_new_password_mail(user, new_password)
        
        user.set_password(new_password);
        user.save()
        
        request.flash['message'] = 'La nueva contraseña ha sido enviada a su correo'
        return HttpResponseRedirect('/')

    except PasswordRegenerationException, e:
        error = str(e)
    except Exception, e:
        error = 'Error desconocido'
        
    return append_ads_to_response(request, 'cotizador/regenerate_password.html', {
        'error': error,
    })
        
@manager_login_required    
def news(request):
    # Shows the logs for the last week
    today = date.today()
    last_logs = LogEntry.objects.filter(date__gte = today - timedelta(days = 1)).order_by('-date').all()
    return append_ads_to_response(request, 'manager/news.html', {
            'last_logs': last_logs,
        })
        
@manager_login_required    
def comments(request):
    # Shows the comments pending for aproval
    due_comments = NotebookComment.objects.filter(validated = False)
    app_comments = NotebookComment.objects.filter(validated = True).filter(date__gte = date.today() - timedelta(days = 2)).order_by('-date').all()
    return append_ads_to_response(request, 'manager/comments.html', {
            'due_comments': due_comments,
            'app_comments': app_comments,            
        })
        
@manager_login_required    
def new_notebooks(request):
    # Shows the models that don't have an associated notebook in the DB (i.e.: pending)
    new_notebooks = StoreHasNotebook.objects.filter(is_available = True).filter(is_hidden = False).filter(notebook = None)
    return append_ads_to_response(request, 'manager/new_notebooks.html', {
            'new_notebooks': new_notebooks,
        })
        
@manager_login_required
def hide_notebook(request, store_has_notebook_id):
    # Makes a model invisible to the "pending" page if it is stupid (e.g. iPad)
    # or doesn't apply (combos of notebooks + printers, notebook sleeves, etc)
    shn = get_object_or_404(StoreHasNotebook, pk = store_has_notebook_id)
    shn.is_hidden = True
    shn.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);

@manager_login_required
def delete_comment(request, comment_id):
    # Deletes a comment
    comment = get_object_or_404(NotebookComment, pk = comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER']);
                       
@manager_login_required                        
def validate_all(request):
    comments = NotebookComment.objects.filter(validated = False)
    for comment in comments:
        comment.validated = True
        comment.save()
    return HttpResponseRedirect('/manager')
            
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
        
    processors = Processor.objects.filter(line__family = processor_line_family).order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/processor_line_family_details.html', {
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
    
    video_cards = VideoCard.objects.filter(line = video_card_line).order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/video_card_line_details.html', {
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
    return append_ads_to_response(request, 'cotizador/all_processor_line_families.html', {
                'processor_line_families': processor_line_families,
                'processors': processors
            })            
            
def all_video_card_lines(request):
    video_card_lines = VideoCardLine.objects.all()
    video_cards = VideoCard.objects.order_by('-speed_score')
    return append_ads_to_response(request, 'cotizador/all_video_card_lines.html', {
                'video_card_lines': video_card_lines,
                'video_cards': video_cards
            })

@manager_login_required            
def analyze_searches(request):
    results = {}
    sf = initialize_search_form(request.GET)
    for field_name, field in sf.fields.items():
        if isinstance(field, ClassChoiceField) or isinstance(field, CustomChoiceField):
            results[field] = {'data': {}, 'meta': {'total': 0}}
        
    srs = SearchRegistry.objects.filter(date__gte = date.today() - timedelta(days = 7)) 
    num_queries = len(srs)
    
    folder = settings.MEDIA_ROOT + '/temp/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass
    
    for sr in srs:
        key_vals = sr.query.split('&')
        for key_val in key_vals:
            vals = key_val.split('=')
            field_name = vals[0]
            field = sf.fields[field_name]
            if not (isinstance(field, ClassChoiceField) or isinstance(field, CustomChoiceField)):
                continue
                
            val = vals[1]
            str_val = field.get_object_name(val)
            if str_val not in results[field]['data']:
                results[field]['data'][str_val] = [0, 0]
            results[field]['data'][str_val][0] += 1
            results[field]['meta']['total'] += 1
            
    for field, field_dict in results.items():
        try: 
            results[field]['meta']['percentage'] = 100.0 * results[field]['meta']['total'] / num_queries
        except:
            results[field]['meta']['percentage'] = 0.0
        sub_total = results[field]['meta']['total']
        for field_option, sub_results in field_dict['data'].items():
            sub_results[1] = 100.0 * sub_results[0] / sub_total
            
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 400)
        chart = PieChart(surface)
                
        dataSet = [(field_option, [[0, sub_results[1]]]) for field_option, sub_results in field_dict['data'].items()]
        if dataSet:
            chart.addDataset(dataSet)
            chart.render()
            filename = folder + str(field.name) + "-" + str(num_queries) + ".png"
            surface.write_to_png(filename)
            results[field]['meta']['is_available'] = True
        else:
            results[field]['meta']['is_available'] = False
            
    return append_ads_to_response(request, 'manager/analyze_searches.html', {
                'form': sf,
                'results': results,
                'num_queries': num_queries,
            })

@login_required    
def subscriptions(request):
    notebook_subscriptions = NotebookSubscription.objects.filter(user = request.user, is_active = True)
    return append_ads_to_response(request, 'account/subscriptions.html', {
        'notebook_subscriptions': notebook_subscriptions,
    })
    
@login_required
def enable_subscription_mail(request, subscription_id):
    set_subscription_mail_notifications(request, subscription_id, True)
    return HttpResponseRedirect('/account')
    
@login_required
def disable_subscription_mail(request, subscription_id):
    set_subscription_mail_notifications(request, subscription_id, False)
    return HttpResponseRedirect('/account')    
    
@login_required
def remove_subscription(request, subscription_id):
    try:
        subscription = NotebookSubscription.objects.get(pk = subscription_id)
        if subscription.user != request.user:
            raise SubscriptionException('Error de seguridad')
        subscription.is_active = False;
        subscription.save()
    except SubscriptionException, e:
        request.flash['error'] = str(e)
    except Exception, e:
        request.flash['error'] = 'Error desconocido'    
    return HttpResponseRedirect('/account')
    
@login_required    
def change_email(request):
    if request.method == 'POST':
        change_email_form = ChangeEmailForm(request.POST)
        user = request.user
        if change_email_form.validate_password_and_form(user):
            new_email = change_email_form.cleaned_data['new_email']            
            user.email = new_email            
            user.is_active = False
            try:
                send_change_mail(user)            
                user.save()
                request.flash['message'] = 'Correo cambiado exitosamente, hemos enviado un mensaje para que pueda activarlo'
            except MailException, e:
                request.flash['error'] = str(e)
            return HttpResponseRedirect('/account/')
    else:
        change_email_form = ChangeEmailForm()
    return append_ads_to_response(request, 'account/change_email.html', {
        'change_email_form': change_email_form,
    })
    
@login_required    
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        user = request.user
        if form.validate_password_and_form(user):
            new_pass = form.cleaned_data['new_password']            
            user.set_password(new_pass);
            user.save()
            request.flash['message'] = 'Contraseña cambiada exitosamente'
            return HttpResponseRedirect('/account/')
    else:
        form = ChangePasswordForm()
    return append_ads_to_response(request, 'account/change_password.html', {
        'p_form': form, })
        
@login_required
def send_confirmation_mail(request):
    if not request.user.is_active:
        try:
            send_signup_mail(request.user)
            request.flash['message'] = 'Correo de validación enviado'
        except MailException, e:
            request.flash['error'] = str(e)            
    else:
        request.flash['message'] = 'Tu cuenta de correo ya está activada'
    return HttpResponseRedirect('/account/')
