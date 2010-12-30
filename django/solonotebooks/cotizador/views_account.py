#-*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from solonotebooks.cotizador.views import append_ads_to_response
from models import *
from fields import *
from exceptions import *
from utils import *
from views import *


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
        return append_ads_to_response(request, 'account/login.html', {
            })
            
@login_required    
def logout(request):
    auth.logout(request)
    next_url = '/'
    if 'next' in request.GET:
        next_url = request.GET['next']
    return HttpResponseRedirect(next_url)
    
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
        
    return append_ads_to_response(request, 'account/regenerate_password.html', {
        'error': error,
    })
    
@login_required    
def subscriptions(request):
    notebook_subscriptions = NotebookSubscription.objects.filter(user = request.user, is_active = True)
    return append_ads_to_response(request, 'account/subscriptions.html', {
        'notebook_subscriptions': notebook_subscriptions,
    })
    
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
def enable_subscription_mail(request):
    subscription_id = request.POST['subscription_id']
    set_subscription_mail_notifications(request, subscription_id, True)
    return HttpResponseRedirect('/account?refresh=true')
        
@login_required
def disable_subscription_mail(request):
    subscription_id = request.POST['subscription_id']
    set_subscription_mail_notifications(request, subscription_id, False)
    return HttpResponseRedirect('/account?refresh=true')
    
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
