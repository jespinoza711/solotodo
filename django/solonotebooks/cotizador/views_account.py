#-*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from solonotebooks.cotizador.views import append_metadata_to_response
import simplejson
from models import *
from fields import *
from exceptions import *
from utils import *
from views import *
import json

def append_account_ptype_to_response(request, template, args):
    tabs = []
    
    name = 'Mis productos'
    url = reverse('solonotebooks.cotizador.views_account.subscriptions')
    tabs.append([-1, name, url])
    
    if request.user.is_authenticated() and not request.user.get_profile().facebook_name:
        name = 'Cambiar correo electrónico'
        url = reverse('solonotebooks.cotizador.views_account.change_email')
        tabs.append([-1, name, url])
        
        name = u'Cambiar contraseña'
        url = reverse('solonotebooks.cotizador.views_account.change_password')
        tabs.append([-1, name, url])
        
        name = 'Fusionar con Facebook'
        url = reverse('solonotebooks.cotizador.views_account.fuse_facebook_account')
        tabs.append([-1, name, url])
    
    args['tabs'] = ['', tabs]
    return append_metadata_to_response(request, template, args)
    
def facebook_login(request):
    response = {
        'code': 'ERROR'
    }

    access_token = request.POST['access_token']
    user_id = request.POST['user_id']

    user = auth.authenticate(user_id=user_id, access_token=access_token)
    if user:
        auth.login(request, user)
        response['code'] = 'OK'
    return HttpResponse(json.dumps(response))
        
def facebook_ajax_login(request):
    response = {'code': 'ERROR'}
    try:
        facebook_cookie_name = 'fbs_' + settings.FACEBOOK_ID
        if facebook_cookie_name in request.COOKIES:
            cookie = request.COOKIES[facebook_cookie_name]
            cookie_info = dict([elem.split('=') for elem in cookie.split('&')])
            uid = cookie_info['uid']
            access_token = cookie_info['access_token']
            
            url = 'https://graph.facebook.com/' + uid + '?access_token=' + access_token
            user_data = simplejson.load(urllib.urlopen(url))
            
            user = auth.authenticate(username = uid, email = user_data['email'], facebook_name = user_data['name'])
            if user:
                auth.login(request, user)
                response['code'] = 'OK'
    except:
        pass
        
    data = simplejson.dumps(response, indent=4)
    return HttpResponse(data, mimetype='application/javascript')  

@login_required        
def facebook_fusion(request):
    next = '/account?refresh=true'
        
    try:
        facebook_cookie_name = 'fbs_' + settings.FACEBOOK_ID
        if facebook_cookie_name in request.COOKIES:
            cookie = request.COOKIES[facebook_cookie_name]
            cookie_info = dict([elem.split('=') for elem in cookie.split('&')])
            uid = cookie_info['uid']
            access_token = cookie_info['access_token']
            
            url = 'https://graph.facebook.com/' + uid + '?access_token=' + access_token
            user_data = simplejson.load(urllib.urlopen(url))
            
            request.user.username = uid
            request.user.email = user_data['email']
            request.user.password = User.objects.make_random_password()
            request.user.save()
            
            profile = request.user.get_profile()
            profile.facebook_name = user_data['name']
            profile.save()
            
            request.flash['message'] = 'Cuentas fusionadas exitosamente'

            return HttpResponseRedirect(next)
        else:
            request.flash['error'] = 'Error fusionando cuentas'
            return HttpResponseRedirect(next)
    except:
        request.flash['error'] = 'Error fusionando cuentas'
        return HttpResponseRedirect(next)
            
@login_required    
def logout(request):
    auth.logout(request)
    
    next_url = '/'
    if 'next' in request.GET:
        next_url = request.GET['next']
    return HttpResponseRedirect(next_url)
    
@login_required    
def subscriptions(request):
    product_subscriptions = ProductSubscription.objects.filter(user = request.user, is_active = True)
    return append_account_ptype_to_response(request, 'account/subscriptions.html', {
        'product_subscriptions': product_subscriptions,
    })
    
@login_required    
def fuse_facebook_account(request):
    return append_account_ptype_to_response(request, 'account/fuse_facebook_account.html', {})
    
@login_required    
def add_subscription(request):
    try:
        product = Product.objects.get(pk = request.GET['product'])
        user = request.user
        
        existing_product_subscriptions = ProductSubscription.objects.filter(user = user).filter(product = product)
        if existing_product_subscriptions:
            product_subscription = existing_product_subscriptions[0]
            product_subscription.is_active = True
        else:
            product_subscription = ProductSubscription()
            product_subscription.user = user
            product_subscription.product = product                                
            
        product_subscription.email_notifications = bool(int(request.GET['email_notifications']))
        product_subscription.save()
        
        request.flash['message'] = 'Suscripción agregada'
    except Exception, e:
        request.flash['error'] = 'Error desconocido'

    return HttpResponseRedirect('/products/' + str(product.id) + '?refresh=true')
    
@login_required
def enable_subscription_mail(request, subscription_id):
    set_subscription_mail_notifications(request, subscription_id, True)
    return HttpResponseRedirect('/account?refresh=true')
        
@login_required
def disable_subscription_mail(request, subscription_id):
    set_subscription_mail_notifications(request, subscription_id, False)
    return HttpResponseRedirect('/account?refresh=true')
    
@login_required
def remove_subscription(request, subscription_id):
    try:
        subscription = ProductSubscription.objects.get(pk = subscription_id)
        if subscription.user != request.user:
            raise SubscriptionException('Error de seguridad')
        subscription.is_active = False;
        subscription.save()
    except SubscriptionException, e:
        request.flash['error'] = str(e)
    except Exception, e:
        request.flash['error'] = 'Error desconocido'    
    return HttpResponseRedirect('/account/?refresh=True')
    
#########################################################################
### Deprecated registration system

# Deprecated    
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
            return HttpResponseRedirect('/account/?refresh=True')
    else:
        change_email_form = ChangeEmailForm()
    return append_account_ptype_to_response(request, 'account/change_email.html', {
        'change_email_form': change_email_form,
    })

# Deprecated    
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
            return HttpResponseRedirect('/account/?refresh=True')
    else:
        form = ChangePasswordForm()
    return append_account_ptype_to_response(request, 'account/change_password.html', {
        'p_form': form, })

# Deprecated        
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
    return HttpResponseRedirect('/account/?refresh=True')

# Deprecated
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
                
            if user.get_profile().facebook_name:
                raise FormException('La cuenta está ligada a un perfil de Facebook, por favor use dicho perfil para ingresar haciendo click en "Entrar con Facebook"')
            
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
    
# Deprecated
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
        return append_metadata_to_response(request, 'account/login.html', {
            })

# Deprecated    
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
        return HttpResponseRedirect('/account/?refresh=True')        
    except MailValidationException, e:
        error = str(e)
    except Exception, e:
        error = 'Error desconocido'
    return append_account_ptype_to_response(request, 'account/validate_email.html', {
            'error': error,
        })
    
# Deprecated    
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
        return HttpResponseRedirect('/?refresh=True')

    except PasswordRegenerationException, e:
        error = str(e)
    except Exception, e:
        error = 'Error desconocido'
        
    return append_account_ptype_to_response(request, 'account/regenerate_password.html', {
        'error': error,
    })
