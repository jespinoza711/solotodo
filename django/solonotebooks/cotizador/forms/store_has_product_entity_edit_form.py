#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from solonotebooks.cotizador.models import Store, Product

class StoreHasProductEntityEditForm(forms.Form):
    product = forms.ModelChoiceField(queryset = Product.get_all_ordered())
    store = forms.ModelChoiceField(queryset = Store.objects.all())
    
    def is_valid(self):
        self.cleaned_data = {}
        self.cleaned_data['product'] = Product.objects.get(pk = self.data['product'])
        self.cleaned_data['store'] = Store.objects.get(pk = self.data['store'])
        print 'wii'
        return True
