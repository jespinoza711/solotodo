#-*- coding: UTF-8 -*-
from django import forms
from solonotebooks import settings

class CompetitivityReportOrdering(forms.Form):
    choices = ((1, 'Nombre'), (2, 'Popularidad en %s ' % settings.SITE_NAME), (3, 'Número de clicks a tiendas'))
    ordering = forms.ChoiceField(choices=choices, label='Ordenar por')
