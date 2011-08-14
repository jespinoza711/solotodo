#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max, Count
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class ProcessorSearchForm(SearchForm):
    brand = ClassChoiceField(ProcessorBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    family = ClassChoiceField(ProcessorFamily, 'Familia', in_quick_search = True, quick_search_name = 'Familia')
    line = ClassChoiceField(ProcessorLine, 'Línea', requires_advanced_controls = True)
    l2_cache = ClassChoiceField(ProcessorL2Cache, 'Caché L2', requires_advanced_controls = True)
    l3_cache = ClassChoiceField(ProcessorL3Cache, 'Caché L3', requires_advanced_controls = True)
    socket = ClassChoiceField(ProcessorSocket, 'Socket', requires_advanced_controls = True)
    core_count = ClassChoiceField(ProcessorCoreCount, 'Nº cores', in_quick_search = True, quick_search_name = 'Número de núcleos')
    core = ClassChoiceField(ProcessorCore, 'Nombre')
    architecture = ClassChoiceField(ProcessorArchitecture, 'Arq.', in_quick_search = True, quick_search_name = 'Arquitectura')
    manufacturing_process = ClassChoiceField(ProcessorManufacturingProcess, 'Proceso', requires_advanced_controls = True)
    
    unlocked_multiplier_choices = (('0', 'Cualquiera'), ('1', 'Bloqueado'), ('2', 'Desbloqueado'))
    unlocked_multiplier = CustomChoiceField(choices = unlocked_multiplier_choices).set_name('Multi.')
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Puntaje Passmark'),
        ('3', 'Puntaje PCMark 05'), 
        ('4', 'Puntaje PCMark Vantage'), 
        ('5', 'Frecuencia'),
        ('6', 'TDP'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 300000, 20000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['brand',
                     'core_count',
                     'family',
                     'line',
                     'socket']],
                 ['Núcleo',
                    ['architecture',
                     'core',
                     'manufacturing_process',]],
                 ['Otros',
                    ['unlocked_multiplier',
                     'l2_cache',
                     'l3_cache']],
                     ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'brand'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(ProcessorBrand.objects.get(pk = pk_value))
        if key == 'family':
            value = unicode(ProcessorFamily.objects.get(pk = pk_value))
        if key == 'line':
            value = unicode(ProcessorLine.objects.get(pk = pk_value))
        if key == 'l2_cache':
            value = u'Caché L2: ' + unicode(ProcessorL2Cache.objects.get(pk = pk_value))
        if key == 'l3_cache':
            value = u'Caché L3: ' + unicode(ProcessorL3Cache.objects.get(pk = pk_value))
        if key == 'socket':
            value = 'Socket ' + unicode(ProcessorSocket.objects.get(pk = pk_value))
        if key == 'core_count':
            value = unicode(ProcessorCoreCount.objects.get(pk = pk_value))
        if key == 'core':
            value = unicode(ProcessorCore.objects.get(pk = pk_value))
        if key == 'architecture':
            value = unicode(ProcessorArchitecture.objects.get(pk = pk_value))
        if key == 'manufacturing_process':
            value = unicode(ProcessorManufacturingProcess.objects.get(pk = pk_value))
        if key == 'unlocked_multiplier':
            value = 'Multiplicador ' + self.unlocked_multiplier_choices[pk_value][1]
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Procesadores ' + unicode(ProcessorBrand.objects.get(pk = pk_value))
        if key == 'family':
            value = 'Procesadores ' + unicode(ProcessorFamily.objects.get(pk = pk_value))
        if key == 'line':
            value = 'Procesadores ' + unicode(ProcessorLine.objects.get(pk = pk_value))
        if key == 'l2_cache':
            value = 'Procesadores con ' + unicode(ProcessorL2Cache.objects.get(pk = pk_value)) + ' de caché L2'
        if key == 'l3_cache':
            value = 'Procesadores con ' + unicode(ProcessorL3Cache.objects.get(pk = pk_value) + 'de caché L3')
        if key == 'socket':
            value = 'Procesadores con socket ' + unicode(ProcessorSocket.objects.get(pk = pk_value))
        if key == 'core_count':
            value = 'Procesadores ' + unicode(ProcessorCoreCount.objects.get(pk = pk_value))
        if key == 'core':
            value = 'Procesadores con núcleo ' + unicode(ProcessorCore.objects.get(pk = pk_value))
        if key == 'architecture':
            value = 'Procesadores con arquitectura ' + unicode(ProcessorArchitecture.objects.get(pk = pk_value))
        if key == 'manufacturing_process':
            value = 'Procesadores de ' + unicode(ProcessorManufacturingProcess.objects.get(pk = pk_value))
        if key == 'unlocked_multiplier':
            value = 'Procesadores con multiplicador ' + self.unlocked_multiplier_choices[pk_value][1]
        return value
        
    def filter_products(self, processors):
        if self.brand:
            processors = processors.filter(line__family__brand = self.brand)
        if self.family:
            processors = processors.filter(line__family = self.family)
        if self.line and self.advanced_controls:
            processors = processors.filter(line = self.line)
        if self.l2_cache and self.advanced_controls:
            processors = processors.filter(l2_cache = self.l2_cache)
        if self.l3_cache and self.advanced_controls:
            processors = processors.filter(l3_cache = self.l3_cache)
        if self.socket and self.advanced_controls:
            processors = processors.filter(socket = self.socket)
        if self.core_count:
            processors = processors.filter(core_count = self.core_count)
        if self.core:
            processors = processors.filter(core = self.core)
        if self.architecture:
            processors = processors.filter(core__architecture = self.architecture)
        if self.manufacturing_process and self.advanced_controls:
            processors = processors.filter(core__manufacturing_process = self.manufacturing_process)
        if self.unlocked_multiplier:
            processors = processors.filter(has_unlocked_multiplier = self.unlocked_multiplier - 1)    
        if self.min_price:
            processors = processors.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            processors = processors.filter(shp__shpe__latest_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            processors = processors.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'passmark_score')
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'pcmark_05_score')
        elif self.ordering == 4:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'pcmark_vantage_score')
        elif self.ordering == 5:
            if ordering_direction == None:
                ordering_direction = '-'    
            processors = processors.order_by(ordering_direction + 'frequency')
        elif self.ordering == 6:
            if ordering_direction == None:
                ordering_direction = ''    
            processors = processors.order_by(ordering_direction + 'tdp')
        else:
            processors = self.handle_extra_ordering(processors)
            
        return processors
