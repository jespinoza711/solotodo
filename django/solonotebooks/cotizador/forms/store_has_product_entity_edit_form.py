#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from solonotebooks.cotizador.models import Store, Product

class StoreHasProductEntityEditForm(forms.Form):
    product = forms.ModelChoiceField(queryset = Product.objects.all())
    store = forms.ModelChoiceField(queryset = Store.objects.all())
