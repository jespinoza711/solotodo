#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class ProcessorSearchForm(SearchForm):
    brand = ClassChoiceField(ProcessorBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    line = ClassChoiceField(ProcessorLine, 'Línea', in_quick_search = True, quick_search_name = 'Línea')
    l2_cache = ClassChoiceField(ProcessorL2Cache, 'Caché L2', requires_advanced_controls = True)
    l3_cache = ClassChoiceField(ProcessorL3Cache, 'Caché L3', requires_advanced_controls = True)
    socket = ClassChoiceField(ProcessorSocket, 'Socket', requires_advanced_controls = True)
    core_count = ClassChoiceField(ProcessorCoreCount, 'Nº cores', in_quick_search = True, quick_search_name = 'Número de núcleos')
    core = ClassChoiceField(ProcessorCore, 'Nombre')
    architecture = ClassChoiceField(ProcessorArchitecture, 'Arquitectura', in_quick_search = True, quick_search_name = 'Arquitectura')
    manufacturing_process = ClassChoiceField(ProcessorManufacturingProcess, 'nm', requires_advanced_controls = True)
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Puntaje PCMark 05'), 
        ('3', 'Puntaje PCMark Vantage'), 
        ('4', 'Puntaje Passmark'),
        ('5', 'Frecuencia'),
        ('6', 'TDP'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 300000, 20000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['brand',
                     'line',
                     'core_count',
                     'socket']],
                 ['Núcleo',
                    ['architecture',
                     'core',
                     'manufacturing_process',
                     'l2_cache',
                     'l3_cache']],
                     ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'line'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(ProcessorBrand.objects.get(pk = pk_value))
        if key == 'line':
            value = unicode(ProcessorLine.objects.get(pk = pk_value))
        if key == 'l2_cache':
            value = unicode(ProcessorL2Cache.objects.get(pk = pk_value))
        if key == 'l3_cache':
            value = unicode(ProcessorL3Cache.objects.get(pk = pk_value))
        if key == 'socket':
            value = unicode(ProcessorSocket.objects.get(pk = pk_value))
        if key == 'core_count':
            value = unicode(ProcessorCoreCount.objects.get(pk = pk_value))
        if key == 'core':
            value = unicode(ProcessorCore.objects.get(pk = pk_value))
        if key == 'architecture':
            value = unicode(ProcessorArchitecture.objects.get(pk = pk_value))
        if key == 'manufacturing_process':
            value = unicode(ProcessorManufacturingProcess.objects.get(pk = pk_value))
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Procesadors ' + unicode(ProcessorBrand.objects.get(pk = pk_value))
        if key == 'line':
            value = 'Procesadors ' + unicode(ProcessorLine.objects.get(pk = pk_value))
        if key == 'l2_cache':
            value = 'Procesadors con ' + unicode(ProcessorL2Cache.objects.get(pk = pk_value)) + ' de caché L2'
        if key == 'l3_cache':
            value = 'Procesadors con ' + unicode(ProcessorL3Cache.objects.get(pk = pk_value) + 'de caché L3')
        if key == 'socket':
            value = 'Procesadors con socket ' + unicode(ProcessorSocket.objects.get(pk = pk_value))
        if key == 'core_count':
            value = 'Procesadors ' + unicode(ProcessorCoreCount.objects.get(pk = pk_value))
        if key == 'core':
            value = 'Procesadors con núcleo ' + unicode(ProcessorCore.objects.get(pk = pk_value))
        if key == 'architecture':
            value = 'Procesadors con arquitectura ' + unicode(ProcessorArchitecture.objects.get(pk = pk_value))
        if key == 'manufacturing_process':
            value = 'Procesadors de ' + unicode(ProcessorManufacturingProcess.objects.get(pk = pk_value))
        return value
        
    def filter_products(self, processors):
        if self.brand:
            processors = processors.filter(line__brand = self.brand)
        if self.line:
            processors = processors.filter(line = self.line)
        if self.l2_cache:
            processors = processors.filter(l2_cache = self.l2_cache)
        if self.l3_cache:
            processors = processors.filter(l3_cache = self.l3_cache)
        if self.socket:
            processors = processors.filter(socket = self.socket)
        if self.core_count:
            processors = processors.filter(core_count = self.core_count)
        if self.core:
            processors = processors.filter(core = self.core)
        if self.architecture:
            processors = processors.filter(core__architecture = self.architecture)
        if self.manufacturing_process:
            processors = processors.filter(core__manufacturing_process = self.manufacturing_process)
        if self.min_price:
            processors = processors.filter(min_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            processors = processors.filter(min_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            processors = processors.order_by(ordering_direction + 'min_price')
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'pcmark_05_score')
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'pcmark_vantage_score')
        elif self.ordering == 4:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'passmark_score')
        elif self.ordering == 5:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'frequency')
        else:
            if ordering_direction == None:
                ordering_direction = ''    
            processors = processors.order_by(ordering_direction + 'tdp')
            
        return processors
