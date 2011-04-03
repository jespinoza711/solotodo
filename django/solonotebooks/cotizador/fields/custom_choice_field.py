from django.forms import ChoiceField
from django import forms

class CustomChoiceField(ChoiceField):
    def get_object_name(self, pk):
        return str(dict(self.choices)[pk])
        
    def set_name(self, name):
        self.name = name
        return self
        
    def does_require_advanced_controls(self):
        self.requires_advanced_controls = True
        return self
        
    def is_in_quick_search(self, name):
        self.in_quick_search = True
        self.quick_search_name = name
        return self
        
    @staticmethod
    def generate_slider(choices):
        first = CustomChoiceField(choices = choices, widget = forms.Select(attrs = {'class': 'custom_range_select'})).set_name('')
        second = CustomChoiceField(choices = choices, widget = forms.Select(attrs = {'class': 'custom_range_select'})).set_name('')
        
        try:
            first.default_slider_value = int(choices[0][0])
            second.default_slider_value = int(choices[-1][0])
        except:
            first.default_slider_value = 0
            second.default_slider_value = 0
        second.has_css_slider = True
        return [first, second]
