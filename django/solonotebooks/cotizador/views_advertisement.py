#-*- coding: UTF-8 -*-
from models import *
from django.utils import simplejson 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from views import append_ads_to_response

def user_store_required(f):
    def wrap(request, *args, **kwargs):
        try:
            store = request.user.get_profile().assigned_store
            if not store:
                return HttpResponseRedirect('/')
            return f(request, store, *args, **kwargs)
        except:
            return HttpResponseRedirect('/')
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

@user_store_required
def manage(request, store):
    return append_ads_to_response(request, 'advertisement/manage.html', {
        'store': store,
    })

@user_store_required
def get_advertisement_options(request, store):
    ntbks = set([shn.notebook for shn in StoreHasNotebook.objects.filter(store = store).filter(is_available = True).filter(is_hidden = False) if shn.notebook])
    
    available_ntbks = []
    publicized_ntbks = []
    taken_ntbks = []
   
    for ntbk in ntbks:
        mini = ntbk.create_miniature()
        shn = ntbk.storehasnotebook_set.filter(store = store).filter(is_available = True).filter(is_hidden = False).order_by('latest_price')[0]
        mini['id'] = shn.id
        mini['store_price'] = shn.latest_price
        mini['external_url'] = shn.url
        
        if not ntbk.publicized_offer:
            available_ntbks.append(mini)
        elif ntbk.publicized_offer.store == store:
            publicized_ntbks.append(mini)
        else:
            taken_ntbks.append(mini)
            
    ntbk_distribution = [available_ntbks, publicized_ntbks, taken_ntbks]
    data = simplejson.dumps(ntbk_distribution, indent = 4)
    return HttpResponse(data, mimetype = 'application/javascript')
    
@user_store_required    
def submit(request, store):
    result = {'code': 'ERROR'}
    try:
        shn = StoreHasNotebook.objects.get(pk = request.POST['id'])
        if shn.store != store:
            raise Exception
            
        if shn.notebook.publicized_offer:
            raise Exception
            
        shn.notebook.publicized_offer = shn
        shn.notebook.save()
        
        result = {'code': 'OK'}
    except Exception, e:
        pass
    data = simplejson.dumps(result, indent = 4)
    return HttpResponse(data, mimetype = 'application/javascript')
    
@user_store_required    
def remove(request, store):
    result = {'code': 'ERROR'}
    try:
        shn = StoreHasNotebook.objects.get(pk = request.POST['id'])
        if shn.store != store:
            raise Exception
            
        if not shn.notebook.publicized_offer:
            raise Exception
            
        shn.notebook.publicized_offer = None
        shn.notebook.save()
        
        result = {'code': 'OK'}
    except Exception, e:
        pass
    data = simplejson.dumps(result, indent = 4)
    return HttpResponse(data, mimetype = 'application/javascript')    
