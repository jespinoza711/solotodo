#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class MotherboardSearchForm(SearchForm):
    brand = ClassChoiceField(MotherboardBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    socket_brand = ClassChoiceField(InterfaceSocketBrand, 'Plataforma', in_quick_search = True, quick_search_name = 'Plataforma')
    northbridge = ClassChoiceField(MotherboardNorthbridge, 'Chipset', in_quick_search = True, quick_search_name = 'Chipset')
    socket = ClassChoiceField(MotherboardSocket, 'Socket', in_quick_search = True, quick_search_name = 'Socket')
    format = ClassChoiceField(MotherboardFormat, 'Formato', requires_advanced_controls = True)
    memory_type = ClassChoiceField(MotherboardMemoryType, 'Tipo')
    memory_channels = ClassChoiceField(MotherboardMemoryChannel, 'Canales')
    integrated_graphics = ClassChoiceField(MotherboardGraphics, 'Integrados')
    
    multi_gpu_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Si'))
    allows_cf = CustomChoiceField(choices = multi_gpu_choices).set_name('CrossFireX').does_require_advanced_controls()
    allows_sli = CustomChoiceField(choices = multi_gpu_choices).set_name('SLI').does_require_advanced_controls()
    
    ordering_choices = (
        ('1', 'Precio'),)
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 300000, 20000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['brand',
                     'socket_brand',
                     'northbridge',
                     'socket',
                     'format',]],
                 ['Memoria',
                    ['memory_type',
                     'memory_channels',]],
                 [u'Gráficos',
                    ['integrated_graphics',
                     'allows_cf',
                     'allows_sli']],
                     ]      
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'socket'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(MotherboardBrand.objects.get(pk = pk_value))
        if key == 'socket_brand':
            value = 'Plataforma ' + unicode(InterfaceSocketBrand.objects.get(pk = pk_value))
        if key == 'northbridge':
            value = 'Chipset ' + unicode(MotherboardNorthbridge.objects.get(pk = pk_value))            
        if key == 'socket':
            value = 'Socket ' + unicode(MotherboardSocket.objects.get(pk = pk_value))
        if key == 'format':
            value = 'Formato ' + unicode(MotherboardFormat.objects.get(pk = pk_value))
        if key == 'memory_type':
            value = 'Soporte memoria ' + unicode(MotherboardMemoryType.objects.get(pk = pk_value))
        if key == 'memory_channels':
            value = 'Soporte memoria ' + unicode(MotherboardMemoryChannel.objects.get(pk = pk_value))
        if key == 'integrated_graphics':
            value = u'Gráficos: ' + unicode(MotherboardGraphics.objects.get(pk = pk_value))
        
        if key == 'allows_cf':
            value = 'CrossFireX: ' + self.multi_gpu_choices[pk_value][1]
        if key == 'allows_sli':
            value = 'SLI: ' + self.multi_gpu_choices[pk_value][1]
        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Placas madre ' + unicode(MotherboardBrand.objects.get(pk = pk_value))
        if key == 'socket_brand':
            value = 'Placas madre con plataforma ' + unicode(InterfaceSocketBrand.objects.get(pk = pk_value))
        if key == 'northbridge':
            value = 'Placas madre con chipset ' + unicode(MotherboardNorthbridge.objects.get(pk = pk_value))
        if key == 'socket':
            value = 'Placas madre con socket ' + unicode(MotherboardSocket.objects.get(pk = pk_value))
        if key == 'format':
            value = 'Placas madre ' + unicode(MotherboardFormat.objects.get(pk = pk_value))
        if key == 'memory_type':
            value = 'Placas madre con soporte de memoria ' + unicode(MotherboardMemoryType.objects.get(pk = pk_value))
        if key == 'memory_channels':
            value = 'Placas madre con soporte de memoria ' + unicode(MotherboardMemoryChannel.objects.get(pk = pk_value))
        if key == 'integrated_graphics':
            value = u'Placas madre con gráficos: ' + unicode(MotherboardGraphics.objects.get(pk = pk_value))
        
        if key == 'allows_cf':
            value = 'Placas madre ' +  ['sin', 'con'][pk_value - 1] + ' soporte para CrossFireX'
        if key == 'allows_sli':
            value = 'Placas madre ' +  ['sin', 'con'][pk_value - 1] + ' soporte para SLI'
        return value
        
    def filter_products(self, motherboards):
        if self.brand:
            motherboards = motherboards.filter(brand = self.brand)
        if self.socket_brand:
            motherboards = motherboards.filter(chipset__northbridge__family__socket__socket__brand = self.socket_brand)
        if self.northbridge:
            motherboards = motherboards.filter(chipset__northbridge = self.northbridge)
        if self.socket:
            motherboards = motherboards.filter(chipset__northbridge__family__socket = self.socket)
        if self.format and self.advanced_controls:
            motherboards = motherboards.filter(format = self.format)
        if self.memory_type:
            motherboards = motherboards.filter(memory_types__mtype__id = self.memory_type).distinct()
        if self.memory_channels:
            motherboards = motherboards.filter(memory_channels = self.memory_channels)
        if self.integrated_graphics:
            motherboards = motherboards.filter(chipset__northbridge__graphics = self.integrated_graphics)
        
        if self.allows_cf and self.advanced_controls:
            motherboards = motherboards.filter(allows_cf = self.allows_cf - 1)
        if self.allows_sli and self.advanced_controls:
            motherboards = motherboards.filter(allows_cf = self.allows_sli - 1)
        if self.min_price:
            motherboards = motherboards.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            motherboards = motherboards.filter(shp__shpe__latest_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            motherboards = motherboards.order_by(ordering_direction + 'shp__shpe__latest_price')
        else:
            motherboards = self.handle_extra_ordering(motherboards)
            
        return motherboards
