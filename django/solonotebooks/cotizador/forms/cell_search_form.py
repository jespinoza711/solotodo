#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class CellSearchForm(SearchForm):
    plan_company = ClassChoiceField(CellCompany, 'Empresa', in_quick_search = True, quick_search_name = 'Empresa')
    
    plan_type_choices = (
        ('0', 'Cualquiera'), 
        ('1', 'Prepago'), 
        ('2', 'Contrato'))
    plan_type = CustomChoiceField(choices = plan_type_choices).set_name('Tipo').is_in_quick_search('Tipo plan')
    
    plan_data_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    plan_data = CustomChoiceField(choices = plan_data_choices).set_name('Datos?').is_in_quick_search('¿Con plan de datos?')
    
    plan_price_choices = SearchForm.generate_price_range(0, 60000, 5000)
    plan_price_min, plan_price_max = CustomChoiceField.generate_slider(plan_price_choices)
    #plan_price_min = CustomChoiceField(choices = plan_price_choices).set_name('min')
    #plan_price_max = CustomChoiceField(choices = plan_price_choices).set_name('max')
    
    manufacturer = ClassChoiceField(CellphoneManufacturer, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    category = ClassChoiceField(CellphoneCategory, 'Categoría')
    form_factor = ClassChoiceField(CellphoneFormFactor, 'Estilo')
    camera = ClassChoiceField(CellphoneCamera, 'Cámara')
    keyboard = ClassChoiceField(CellphoneCategory, 'Teclado')
    operating_system = ClassChoiceField(CellphoneOperatingSystem, 'Sist. Op.')
    
    screen_size = ClassChoiceField(CellphoneScreenSize, 'Tam. mín.')
    screen_touch_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    screen_touch = CustomChoiceField(choices = screen_touch_choices).set_name('Táctil')
    
    comm_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    has_3g = CustomChoiceField(choices = comm_choices).set_name('3G')
    has_bluetooth = CustomChoiceField(choices = comm_choices).set_name('Bluetooth')
    has_wifi = CustomChoiceField(choices = comm_choices).set_name('WiFi')
    has_gps = CustomChoiceField(choices = comm_choices).set_name('GPS')
    
    ram = ClassChoiceField(CellphoneRam, 'RAM')
    processor = ClassChoiceField(CellphoneProcessor, 'Procesador')
    graphics = ClassChoiceField(CellphoneGraphics, 'Gráficos')
    
    ordering_choices = (
        ('1', 'Precio equipo'), 
        ('2', 'Costo a 3 meses'),
        ('3', 'Costo a 6 meses'), 
        ('4', 'Costo a 12 meses'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 250000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos plan',
                    ['plan_company',
                     'plan_type',
                     'plan_data',
                     'plan_price_min',
                     'plan_price_max']],
                 ['Datos celular',
                    ['manufacturer',
                     'category',
                     'form_factor',
                     'camera',
                     'keyboard',
                     'operating_system',
                     ]],
                 ['Comunicaciones',
                    ['has_3g',
                     'has_bluetooth',
                     'has_wifi',
                     'has_gps'
                     ]],
                 ['Avanzado',
                    ['ram',
                     'processor',
                     'graphics',
                     ]],
                     ]
                     
        return self.parse_model(model)
        
    def __init__(self, qd):
        if 'plan_price_min' not in qd:
            qd['plan_price_min'] = 0
        if 'plan_price_max' not in qd:
            qd['plan_price_max'] = self.plan_price_choices[-1][0]
        super(CellSearchForm, self).__init__(qd)
        
    def main_category_string(self):
        return 'plan_company'    

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
        
    def filter_products(self, cells):
        '''
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
            processors = processors.order_by(ordering_direction + 'shp__shpe__latest_price')
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
        else:
            if ordering_direction == None:
                ordering_direction = ''    
            processors = processors.order_by(ordering_direction + 'tdp')
        '''
            
        return cells
        
