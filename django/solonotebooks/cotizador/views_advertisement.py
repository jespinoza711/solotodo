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
from solonotebooks.cotizador.views import append_ads_to_response
from models import *
from fields import *
from exceptions import *
from utils import *

def append_advertisement_ptype_to_response(request, template, args):
    args['ptypes'] = ProductType.objects.all()
    return append_ads_to_response(request, template, args)

def store_user_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.get_profile().assigned_store:
            request.flash['error'] = 'Por favor inicie sesión primero'
            return HttpResponseRedirect('/')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
    
@store_user_required
def index(request):
    store = request.user.get_profile().assigned_store
    shpes = StoreHasProductEntity.objects.filter(store = store, is_available = True)
    
    non_indexable_shpes = shpes.filter(is_hidden = True)
    shpes = shpes.filter(is_hidden = False)
    
    non_indexed_shpes = shpes.filter(shp__isnull = True)
    shpes = shpes.filter(shp__isnull = False)
    
    product_pairs = list(set([(shpe, shpe.shp.product) for shpe in shpes if shpe.shp.product.ptype.classname == 'Notebook']))
    
    unavailable_products = []
    reserved_products = []
    free_products = []
    
    for product_pair in product_pairs:
        product = product_pair[1]
        if not product.sponsored_shp:
            free_products.append(product_pair)
        elif product.shp.shpe.store == store:
            used_products.append(product_pair)
        else:
            unavailable_products.append(product_pair)            
    
    return append_advertisement_ptype_to_response(request, 'advertisement/index.html', {
        'store': store,
        'non_indexable_shpes': non_indexable_shpes,
        'non_indexed_shpes': non_indexed_shpes,
        'unavailable_products': unavailable_products,
        'reserved_products': reserved_products,
        'free_products': free_products
    })
    
    
