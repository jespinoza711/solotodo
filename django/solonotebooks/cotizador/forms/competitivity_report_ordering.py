#-*- coding: UTF-8 -*-
from django import forms
from solonotebooks import settings

class CompetitivityReportOrdering(forms.Form):
    choices = ((1, u'Nombre'), (2, u'Popularidad en %s ' % settings.SITE_NAME), (3, u'Número de clicks a tiendas'))
    ordering = forms.ChoiceField(choices=choices, label='Ordenar por')
    
    def get_ordering_as_string(self):
        if self.is_valid():
            d = dict(self.fields['ordering'].choices)
            return d[int(self.cleaned_data['ordering'])]
        else:
            return self.fields['ordering'].choices[0][1]
