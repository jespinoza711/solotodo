#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class ScreenSearchForm(SearchForm):
    screen_type = ClassChoiceField(ScreenType, 'Categoría', in_quick_search = True, quick_search_name = 'Categoría')
    brand = ClassChoiceField(ScreenBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    display = ClassChoiceField(ScreenDisplay, 'Tipo av.')
    display_type = ClassChoiceField(ScreenDisplayType, 'Tipo', in_quick_search = True, quick_search_name = 'Tipo')
    min_size = ClassChoiceField(ScreenSizeFamily, 'Mín')
    max_size = ClassChoiceField(ScreenSizeFamily, 'Max')
    resolution = ClassChoiceField(ScreenResolution, 'Resolución', in_quick_search = True, quick_search_name = 'Resolución')
    panel_type = ClassChoiceField(ScreenPanelType, 'Panel')
    response_time = ClassChoiceField(ScreenResponseTime, 'T. resp.')
    
    digital_tuner_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    digital_tuner = CustomChoiceField(choices = digital_tuner_choices).set_name('Digital')
    
    analog_tuner_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    analog_tuner = CustomChoiceField(choices = analog_tuner_choices).set_name('Análogo')
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Tamaño'),
        ('3', 'Resolución'),
        ('4', 'Contraste'),
        ('5', 'Tiempo de respuesta'),
        )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 1000000, 50000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['screen_type',
                     'brand',
                     'display_type',
                     'display',]],
                 ['Tamaño',
                    ['min_size',
                     'max_size',
                     'resolution',]],
                 ['Sintonizadores',
                    ['analog_tuner',
                     'digital_tuner',]],
                 ['Otros',
                    ['response_time',
                     'panel_type',]],
                     ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'screen_type'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(ScreenBrand.objects.get(pk = pk_value))
        if key == 'display':
            value = unicode(ScreenDisplay.objects.get(pk = pk_value))
        if key == 'display_type':
            value = unicode(ScreenDisplayType.objects.get(pk = pk_value))
        if key == 'screen_type':
            value = unicode(ScreenType.objects.get(pk = pk_value))
        if key == 'min_size':
            value = unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'max_size':
            value = unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'resolution':
            value = unicode(ScreenResolution.objects.get(pk = pk_value))
        if key == 'panel_type':
            value = unicode(ScreenPanelType.objects.get(pk = pk_value))
        if key == 'response_time':
            value = unicode(ScreenResponseTime.objects.get(pk = pk_value))
        if key == 'has_analog_tuner':
            value = 'Sintonizador análogo: ' + self.analog_tuner_choices[pk_value][1]
        if key == 'has_digital_tuner':
            value = 'Sintonizador digital: ' + self.digital_tuner_choices[pk_value][1]
        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Pantallas ' + unicode(ScreenBrand.objects.get(pk = pk_value))
        if key == 'display':
            value = 'Pantallas ' + unicode(ScreenDisplay.objects.get(pk = pk_value))
        if key == 'display_type':
            value = 'Pantallas ' + unicode(ScreenDisplayType.objects.get(pk = pk_value))
        if key == 'screen_type':
            value = unicode(ScreenType.objects.get(pk = pk_value))
        if key == 'min_size':
            value = 'Pantallas con tamaño mínimo de ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value)) + ' pulgadas'
        if key == 'max_size':
            value = 'Pantallas con tamaño máximo de ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value)) + ' pulgadas'
        if key == 'resolution':
            value = 'Pantallas con resolución de ' + unicode(ScreenResolution.objects.get(pk = pk_value))
        if key == 'panel_type':
            value = 'Pantallas con paneles ' + unicode(ScreenPanelType.objects.get(pk = pk_value))
        if key == 'response_time':
            value = 'Pantallas con tiempo de respuesta de ' + unicode(ScreenResponseTime.objects.get(pk = pk_value))
        if key == 'has_analog_tuner':
            value = 'Pantallas ' + ['sin', 'con'][pk_value][1] + ' sintonizador análogo'
        if key == 'has_digital_tuner':
            value = 'Pantallas ' + ['sin', 'con'][pk_value][1] + ' sintonizador digital'
        return value
        
    def filter_products(self, screens):
        if self.brand:
            screens = screens.filter(line__brand = self.brand)
        if self.display:
            screens = screens.filter(display = self.display)
        if self.display_type:
            screens = screens.filter(display__type = self.display_type)
        if self.screen_type:
            screens = screens.filter(stype = self.screen_type)
        if self.min_size:
            screens = screens.filter(size__value__gte = ScreenSizeFamily.objects.get(pk = self.min_size).value)
        if self.max_size:
            screens = screens.filter(size__value__lte = ScreenSizeFamily.objects.get(pk = self.max_size).value)
        if self.resolution:
            screens = screens.filter(resolution = self.resolution)
        if self.panel_type:
            screens = screens.filter(panel_type = self.panel_type)
        if self.response_time:
            screens = screens.filter(response_time = self.response_time)
        if self.analog_tuner:
            screens = screens.filter(has_analog_tuner = self.analog_tuner - 1)
        if self.digital_tuner:
            screens = screens.filter(digital_tuner = self.digital_tuner - 1)
        if self.min_price:
            screens = screens.filter(min_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            screens = screens.filter(min_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            screens = screens.order_by(ordering_direction + 'min_price')
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = '-'
            screens = screens.order_by(ordering_direction + 'size')
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = '-'    
            screens = screens.order_by(ordering_direction + 'resolution')
        elif self.ordering == 4:
            if ordering_direction == None:
                ordering_direction = '-'    
            screens = screens.order_by(ordering_direction + 'contrast')
        else:
            if ordering_direction == None:
                ordering_direction = ''
            screens = screens.order_by(ordering_direction + 'response_time')
            
        return screens
