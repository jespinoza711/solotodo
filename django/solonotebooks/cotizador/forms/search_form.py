#-*- coding: UTF-8 -*-
from django import forms
from solonotebooks.cotizador.fields import *
from solonotebooks.cotizador.models.utils import prettyPrice
from solonotebooks.cotizador.models import SearchRegistry
from django.forms.forms import BoundField
from datetime import date

class SearchForm(forms.Form):
    ordering_direction = forms.IntegerField(widget = forms.HiddenInput())
    advanced_controls = forms.IntegerField(widget = forms.HiddenInput())
    page_number = forms.IntegerField()
    
    list_unavailable_products_choices = (('0', 'No'), ('1', 'Sí'))
    list_unavailable_products = CustomChoiceField(choices = list_unavailable_products_choices).set_name('Mostrar todos?').does_require_advanced_controls()
    
    def filter(self, classname):
        if self.list_unavailable_products:
            products = classname.objects.all()
        else:
            products = classname.objects.filter(shp__isnull = False)
        return self.filter_products(products)
    
    def __init__(self, qd, extra_permissions):
        if 'max_price' not in qd:
            qd['max_price'] = self.price_choices[-1][0]
        if 'min_price' not in qd:
            qd['min_price'] = self.price_choices[0][0]
        if 'ordering' not in qd:
            qd['ordering'] = '1'
        
        if extra_permissions:
            default_ordering_choices = self.ordering_choices
            last_ordering_index = int(default_ordering_choices[-1][0])
            new_ordering_choices = list(default_ordering_choices)
            
            new_ordering_choice = (str(last_ordering_index + 1), u'Popularidad en SoloTodo')
            new_ordering_choices.append(new_ordering_choice)
            
            new_ordering_choice = (str(last_ordering_index + 2), u'Número de clicks a tiendas')
            new_ordering_choices.append(new_ordering_choice)
            
            self.ordering_choices = tuple(new_ordering_choices)
            
        super(SearchForm, self).__init__(qd)
        
    def handle_extra_ordering(self, products):
        last_ordering_index = int(self.ordering_choices[-1][0])
        
        if self.ordering == last_ordering_index - 1:
            products = products.order_by('-week_visitor_count')
        elif self.ordering == last_ordering_index:
            products = products.order_by('-week_external_visits')
            
        return products
        
    @staticmethod
    def generate_price_range(mini, maxi, step):
        result = []
        value = mini
        while value <= maxi:
            result.append([str(value), prettyPrice(value, show_symbol = False)])
            value += step
        result[-1][1] += '+'
        return result
        
    def is_valid(self):
        return True 
        
    def generate_title(self):
        # We are going to skip the special "filters" as they don't apply
        skip_keys = ['page_number', 'advanced_controls', 'ordering', 'ordering_direction', 'min_price', 'max_price', 'list_unavailable_products']
        valid_keys = []
        
        # For each filter (including those not active, represented by empty)
        adv_fields = self.get_attributes_requiring_advanced_controls()
        slider_fields = self.get_slider_attributes()
        
        for key in self.fields:
            if key in skip_keys:
                continue
                
            # If this filter requires advanced controls, but they are not activated, skip
            if not self.advanced_controls and key in adv_fields:
                continue
                
            if key in slider_fields and self.__dict__[key] == self.fields[key].default_slider_value:
                continue
    
            # If the filter is active (i.e., its value is not empty)...
            if key in self.__dict__ and self.__dict__[key]:
                valid_keys.append(key)
        
        if len(valid_keys) == 0:
            return 'Catálogo de productos'
        elif len(valid_keys) == 1:
            value = self.generate_title_tag(valid_keys[0], self.__dict__[valid_keys[0]])
            return value
        else: 
            return 'Resultados de la búsqueda'
        
    def save(self):
        query = '&'.join([field + '=' + str(self.__dict__[field]) for field in self.fields if self.__dict__[field]])
        search_registry = SearchRegistry()
        search_registry.query = query
        search_registry.date = date.today()
        search_registry.save()
            
    def main_category(self):
        return self.fields[self.main_category_string()]
        
        
    def main_category_key(self):
        return self.__dict__[self.main_category_string()]
        
    def main_category_bound_field(self):
        return BoundField(self, self.main_category(), self.main_category_string())        
        
    def get_attributes_requiring_advanced_controls(self):
        result = []
        for key, field in self.fields.items():
            try:
                if field.requires_advanced_controls:
                    result.append(key)
            except:
                continue
        return result
        
    def get_slider_attributes(self):
        result = []
        for key, field in self.fields.items():
            try:
                if field.default_slider_value:
                    result.append(key)
            except:
                continue
        return result
            

    def get_quick_search_fields(self):
        quick_search_fields = []
        
        for field_name, field in self.fields.items():
            try:
                if field.in_quick_search:
                    quick_search_fields.append([field.quick_search_name, self[field_name]])
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
        
    def validate(self):
        fields = [[field_name, self.fields[field_name]] for field_name in self.fields]
    
        # First we validate the ClassChoiceFields
        class_choice_fields = filter(lambda x: isinstance(x[1], forms.ModelChoiceField), fields)
        
        for pair in class_choice_fields:
            try:
                choice_field_selection_id = int(self.data[pair[0]])
                field_selection_instance = pair[1].class_name.objects.get(pk = choice_field_selection_id)  
                self.__dict__[pair[0]] = choice_field_selection_id
            except:
                self.__dict__[pair[0]] = 0
                
        # ModelChoiceFields are a subclass of ChoiceField, so we need to remove
        # them from fields to prevent them from processing again
        
        fields = filter(lambda x: x not in class_choice_fields, fields)
        choice_fields = filter(lambda x: isinstance(x[1], forms.ChoiceField), fields)
        
        for pair in choice_fields:
            try:
                choice_field_selection = self.data[pair[0]]
                
                if pair[0] == 'ordering':
                    choices_dict = dict(self.ordering_choices)
                else:
                    choices_dict = dict([[x[0], x[1]] for x in self.fields[pair[0]].choices])
                
                if not choice_field_selection in choices_dict:
                    choice_field_selection = 0
                
                self.__dict__[pair[0]] = int(choice_field_selection)
            except:
                self.__dict__[pair[0]] = 0
                
        integer_fields = filter(lambda x: isinstance(x[1], forms.IntegerField), fields)
        
        for pair in integer_fields:
            try:
                integer_field_value = int(self.data[pair[0]])
                self.__dict__[pair[0]] = integer_field_value
            except:
                self.__dict__[pair[0]] = 0
                
        # Particular cases
        if not self.ordering_direction in [0, 1, 2]:
            self.ordering_direction = 0
            
        if not self.advanced_controls in [0, 1]:
            self.advanced_controls = 0
            
        if self.page_number <= 0:
            self.page_number = 1
            
        if self.ordering == 0:
            self.ordering = 1
        
    def get_ordering_options(self):
        return self.ordering_choices
        
    def generate_current_url_with_skip(self, skip_keys, start_symbol = '?'):
        keyvalues = []
        for key in self.fields:
            if key not in self.__dict__ or not self.__dict__[key] or key in skip_keys:
                continue
            keyvalues.append(key + '=' + str(self.__dict__[key]))
        return start_symbol + '&'.join(keyvalues)
        
    def generate_url_without_ordering(self):
        return self.generate_current_url_with_skip(['page_number', 'ordering', 'ordering_direction']) + '&ordering='
   
    def generate_url_without_main_category(self):
        return self.generate_current_url_with_skip(['page_number', self.main_category_string()], '')
        
    def generate_base_page_link(self):
        return self.generate_current_url_with_skip(['page_number']) + '&page_number='
        
    def generate_remove_filter_links(self):
        filters = {}
        
        # We are going to skip the special "filters" as they don't apply
        skip_keys = ['page_number', 'ordering', 'ordering_direction', 'min_price', 'max_price', 'advanced_controls', 'list_unavailable_products']
        
        # For each filter (including those not active, represented by empty)
        adv_fields = self.get_attributes_requiring_advanced_controls()
        slider_fields = self.get_slider_attributes()
        for key in self.fields:
            if key in skip_keys:
                continue
                
            # If this filter requires advanced controls, but they are not activated, skip
            if not self.advanced_controls and key in adv_fields:
                continue
                
            if key in slider_fields and self.__dict__[key] == self.fields[key].default_slider_value:
                continue
    
            # If the filter is active (i.e., its value is not empty)...
            if key in self.__dict__ and self.__dict__[key]:
                # Create its matching string and link and add it to the list
                filters[self.get_key_data_value(key, self.__dict__[key])] = self.generate_current_url_with_skip([key])
        return filters
