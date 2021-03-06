#-*- coding: UTF-8 -*-
# Class that represents the search form to find screens
from django import forms
from django.db.models import Count
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from . import SearchForm

class ScreenSearchForm(SearchForm):
    screen_type = ClassChoiceField(ScreenType, 'Categoría', in_quick_search = True, quick_search_name = 'Categoría')
    brand = ClassChoiceField(ScreenBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    display = ClassChoiceField(ScreenDisplay, 'Tipo')
    min_size, max_size = ClassChoiceField.generate_slider(ScreenSizeFamily)
    resolution = ClassChoiceField(ScreenResolution, 'Resolución', in_quick_search = True, quick_search_name = 'Resolución')
    panel_type = ClassChoiceField(ScreenPanelType, 'Panel', requires_advanced_controls = True)
    response_time = ClassChoiceField(ScreenResponseTime, 'T. resp.')
    refresh_rate = ClassChoiceField(ScreenRefreshRate, 'Refresco', requires_advanced_controls = True)
    video_port = ClassChoiceField(ScreenVideoPort, 'Puerto')
    
    digital_tuner = ClassChoiceField(ScreenDigitalTuner, 'Digital')
    
    analog_tuner_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Si'))
    analog_tuner = CustomChoiceField(choices = analog_tuner_choices).set_name('Análogo')
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Tamaño'),
        ('3', 'Resolución'),
        ('4', 'Tiempo de respuesta'),
        )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 800000, 50000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['display',
                     'resolution',
                     'brand'
                     ]],
                 ['Tamaño',
                    ['min_size',
                     'max_size',]],
                 ['Sintonizadores',
                    ['digital_tuner',
                     'analog_tuner',
                    ]],
                 ['Otros',
                    ['video_port',
                     'response_time',
                     'refresh_rate',
                     'panel_type',]],
                     ]
                     
        return self.parse_model(model)
        
    def __init__(self, qd, extra_permissions):
        if 'max_size' not in qd:
            qd['max_size'] = ScreenSizeFamily.objects.reverse()[0].id
        if 'min_size' not in qd:
            qd['min_size'] = ScreenSizeFamily.objects.all()[0].id
        super(ScreenSearchForm, self).__init__(qd, extra_permissions)
        
    def main_category_string(self):
        return 'screen_type' 

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(ScreenBrand.objects.get(pk = pk_value))
        if key == 'display':
            value = unicode(ScreenDisplay.objects.get(pk = pk_value))
        if key == 'screen_type':
            value = unicode(ScreenType.objects.get(pk = pk_value))
        if key == 'min_size':
            value = u'Tamaño mínimo: ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'max_size':
            value = u'Tamaño máximo: ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'resolution':
            value = u'Resolución mínima: ' + unicode(ScreenResolution.objects.get(pk = pk_value))
        if key == 'panel_type':
            value = 'Panel ' + unicode(ScreenPanelType.objects.get(pk = pk_value))
        if key == 'response_time':
            value = u'T. de respuesta max.: ' + unicode(ScreenResponseTime.objects.get(pk = pk_value))
        if key == 'refresh_rate':
            value = u'T. de refresco mínima.: ' + unicode(ScreenRefreshRate.objects.get(pk = pk_value))
        if key == 'analog_tuner':
            choice = self.analog_tuner_choices[pk_value][1]
            value = u'Sintonizador análogo: ' + choice
        if key == 'digital_tuner':
            value = 'Sintonizador digital: ' + unicode(ScreenDigitalTuner.objects.get(pk = pk_value))
        if key == 'video_port':
            value = u'Con puerto de video: ' + unicode(ScreenVideoPort.objects.get(pk = pk_value))                
        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Pantallas ' + unicode(ScreenBrand.objects.get(pk = pk_value))
        if key == 'display':
            value = 'Pantallas ' + unicode(ScreenDisplay.objects.get(pk = pk_value))
        if key == 'screen_type':
            value = unicode(ScreenType.objects.get(pk = pk_value))
        if key == 'min_size':
            value = u'Pantallas con tamaño mínimo de ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'max_size':
            value = u'Pantallas con tamaño máximo de ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'resolution':
            value = u'Pantallas con resolución mínima ' + unicode(ScreenResolution.objects.get(pk = pk_value))
        if key == 'panel_type':
            value = 'Pantallas con paneles ' + unicode(ScreenPanelType.objects.get(pk = pk_value))
        if key == 'response_time':
            value = u'Pantallas con tiempo de respuesta máximo de ' + unicode(ScreenResponseTime.objects.get(pk = pk_value))
        if key == 'refresh_rate':
            value = u'Pantallas con tasa de refresco mínima de ' + unicode(ScreenRefreshRate.objects.get(pk = pk_value))
        if key == 'analog_tuner':
            value = 'Pantallas ' + ['sin', 'con'][pk_value - 1] + u' sintonizador análogo'
        if key == 'digital_tuner':
            value = 'Pantallas con sintonizador digital: ' + unicode(ScreenDigitalTuner.objects.get(pk = pk_value))
        if key == 'video_port':
            value = u'Pantallas con puerto de video ' + unicode(ScreenVideoPort.objects.get(pk = pk_value)) 
        return value
        
    def filter_products(self, screens):
        if self.brand:
            screens = screens.filter(line__brand = self.brand)
        if self.display:
            screens = screens.filter(display = self.display)
        if self.screen_type:
            screens = screens.filter(stype = self.screen_type)
        if self.min_size:
            screens = screens.filter(size__family__value__gte = ScreenSizeFamily.objects.get(pk = self.min_size).value)
        if self.max_size:
            screens = screens.filter(size__family__value__lte = ScreenSizeFamily.objects.get(pk = self.max_size).value)
        if self.resolution:
            screens = screens.filter(resolution__total_pixels__gte = ScreenResolution.objects.get(pk = self.resolution).total_pixels)
        if self.panel_type and self.advanced_controls:
            screens = screens.filter(panel_type = self.panel_type)
        if self.response_time:
            screens = screens.filter(response_time__value__lte = ScreenResponseTime.objects.get(pk = self.response_time).value)
        if self.refresh_rate and self.advanced_controls:
            screens = screens.filter(refresh_rate__value__gte = ScreenRefreshRate.objects.get(pk = self.refresh_rate).value)
        if self.analog_tuner:
            screens = screens.filter(has_analog_tuner = self.analog_tuner - 1)
        if self.digital_tuner:
            screens = screens.filter(digital_tuner = self.digital_tuner)
        if self.min_price:
            screens = screens.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            screens = screens.filter(shp__shpe__latest_price__lte = int(self.max_price))
        if self.video_port:
            screens = screens.filter(video_ports__port__id = self.video_port).distinct()
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction is None:
                ordering_direction = ''
            screens = screens.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction is None:
                ordering_direction = '-'
            screens = screens.order_by(ordering_direction + 'size')
        elif self.ordering == 3:
            if ordering_direction is None:
                ordering_direction = '-'    
            screens = screens.order_by(ordering_direction + 'resolution')
        elif self.ordering == 4:
            if ordering_direction is None:
                ordering_direction = ''
            screens = screens.order_by(ordering_direction + 'response_time')
        else:
            screens = self.handle_extra_ordering(screens)
            
        return screens
