#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList

class SearchShpeForm(forms.Form):
    url = forms.CharField(max_length = 255, label='URL')
