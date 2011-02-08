from django import forms
from solonotebooks.cotizador.fields import *

class SearchForm(forms.Form):
    def __init__(self, qd):
        if 'max_price' not in qd:
            qd['max_price'] = self.price_choices[-1][0]
        if 'min_price' not in qd:
            qd['min_price'] = self.price_choices[0][0]
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
