#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from solonotebooks.cotizador.models import Store, Notebook

class StoreHasProductEntityEditForm(forms.Form):
    notebook = forms.ModelChoiceField(queryset = Notebook.objects.all())
    store = forms.ModelChoiceField(queryset = Store.objects.all())
