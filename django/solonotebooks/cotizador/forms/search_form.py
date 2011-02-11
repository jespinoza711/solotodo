from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.fields import *
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils

class SearchForm(forms.Form):
    def __init__(self, qd):
        if 'max_price' not in qd:
            qd['max_price'] = utils.roundToCeil10000(Notebook.objects.filter(is_available = True).aggregate(Max('min_price'))['min_price__max'])
        if 'min_price' not in qd:
            qd['min_price'] = utils.roundToFloor10000(Notebook.objects.filter(is_available = True).aggregate(Min('min_price'))['min_price__min'])
        if 'ordering' not in qd:
            qd['ordering'] = '1'
        super(SearchForm, self).__init__(qd)

    def get_quick_search_fields(self):
        quick_search_fields = []
        class_whitelist = [ClassChoiceField, CustomChoiceField]
        
        for field_name, field in self.fields.items():
            try:
                if field.in_quick_search:
                    quick_search_fields.append([field.name, self[field_name]])
            except:
                continue
        return quick_search_fields
        
    def parse_model(self, model):
        result = []
        
        for submodel in model:
            step = [submodel[0]]
            fields = []
            for field in submodel[1]:
                fields.append([self.fields[field], self[field]])
            step.append(fields)
            result.append(step)
        
        return result
