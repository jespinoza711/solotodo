#-*- coding: UTF-8 -*-
# Class that represents the search form to find video cards
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class VideoCardSearchForm(SearchForm):
    gpu_brand = ClassChoiceField(VideoCardGpuBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    gpu_family = ClassChoiceField(VideoCardGpuFamily, 'Familia', in_quick_search = True, quick_search_name = 'Familia')
    brand = ClassChoiceField(VideoCardBrand, 'Fabricante', requires_advanced_controls = True)
    gpu_line = ClassChoiceField(VideoCardGpuLine, 'Línea')
    gpu = ClassChoiceField(VideoCardGpu, 'Modelo', in_quick_search = True, quick_search_name = 'GPU')
    gpu_core_count = ClassChoiceField(VideoCardGpuCoreCount, 'Núcleos', requires_advanced_controls = True)
    memory_quantity = ClassChoiceField(VideoCardMemoryQuantity, 'Cant. mín', in_quick_search = True, quick_search_name = 'Memoria')
    memory_type = ClassChoiceField(VideoCardMemoryType, 'Tipo', requires_advanced_controls = True)
    memory_bus_width = ClassChoiceField(VideoCardMemoryBusWidth, 'Ancho', requires_advanced_controls = True)
    gpu_architecture = ClassChoiceField(VideoCardGpuArchitecture, 'Nombre')
    gpu_core_family = ClassChoiceField(VideoCardGpuCoreFamily, 'Familia')
    gpu_dx_version = ClassChoiceField(VideoCardGpuDirectxVersion, 'DirectX', requires_advanced_controls = True)
    gpu_ogl_version = ClassChoiceField(VideoCardGpuOpenglVersion, 'OpenGL', requires_advanced_controls = True)
    bus_name = ClassChoiceField(VideoCardBusName, 'Nombre')
    bus_lanes = ClassChoiceField(VideoCardBusLane, 'Lanes', requires_advanced_controls = True)
    bus = ClassChoiceField(VideoCardBus, 'Bus', requires_advanced_controls = True)
    profile = ClassChoiceField(VideoCardProfile, 'Perfil')
    refrigeration = ClassChoiceField(VideoCardRefrigeration, 'Cooling', requires_advanced_controls = True)
    slots = ClassChoiceField(VideoCardSlotType, 'Slots', requires_advanced_controls = True)
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Puntaje 3DMark06'), 
        ('3', 'Puntaje 3DMark Vantage'), 
        ('4', 'Puntaje 3DMark 11'),
        ('5', 'Cantidad de memoria'), 
        ('6', 'TDP'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 500000, 25000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['gpu_brand',
                     'gpu_family',
                     'brand',]],
                 ['GPU',
                    ['gpu_line',
                     'gpu',
                     'gpu_core_count']],
                 ['Memoria',
                    ['memory_quantity',
                    'memory_type',
                    'memory_bus_width',]],
                 ['Arquitectura',
                    ['gpu_architecture',
                     'gpu_core_family',
                     'gpu_dx_version',
                     'gpu_ogl_version',]],
                 ['Bus',
                    ['bus_name',
                     'bus_lanes',
                     'bus']],
                 ['Otros',
                    ['profile',
                     'refrigeration',
                     'slots',]],
                     ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'gpu_family'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'gpu_brand':
            value = unicode(VideoCardGpuBrand.objects.get(pk = pk_value))
        if key == 'gpu_family':
            value = unicode(VideoCardGpuLineFamily.objects.get(pk = pk_value))
        if key == 'brand':
            value = unicode(VideoCardBrand.objects.get(pk = pk_value))
        if key == 'gpu_line':
            value = unicode(VideoCardGpuLine.objects.get(pk = pk_value))
        if key == 'gpu':
            value = unicode(VideoCardGpu.objects.get(pk = pk_value))
        if key == 'gpu_core_count':
            value = unicode(VideoCardGpuCoreCount.objects.get(pk = pk_value))
        if key == 'memory_quantity':
            value = unicode(VideoCardMemoryQuantity.objects.get(pk = pk_value))
        if key == 'memory_type':
            value = unicode(VideoCardMemoryType.objects.get(pk = pk_value))
        if key == 'memory_bus_width':
            value = unicode(VideoCardMemoryBusWidth.objects.get(pk = pk_value))
        if key == 'gpu_architecture':
            value = unicode(VideoCardGpuArchitecture.objects.get(pk = pk_value))
        if key == 'gpu_core_family':
            value = unicode(VideoCardGpuCoreFamily.objects.get(pk = pk_value))
        if key == 'gpu_dx_version':
            value = unicode(VideoCardGpuDirecxVersion.objects.get(pk = pk_value))
        if key == 'gpu_ogl_version':
            value = unicode(VideoCardGpuOpenglVersion.objects.get(pk = pk_value))
        if key == 'bus_name':
            value = unicode(VideoCardBusName.objects.get(pk = pk_value))
        if key == 'bus_lanes':
            value = unicode(VideoCardBusLane.objects.get(pk = pk_value))
        if key == 'bus':
            value = unicode(VideoCardBus.objects.get(pk = pk_value))
        if key == 'profile':
            value = unicode(VideoCardProfile.objects.get(pk = pk_value))
        if key == 'refrigeration':
            value = unicode(VideoCardRefrigeration.objects.get(pk = pk_value))
        if key == 'slots':
            value = unicode(VideoCardSlotType.objects.get(pk = pk_value))
        if key == 'min_price':
            value = 'Precio minimo: ' + utils.prettyPrice(pk_value)
        if key == 'max_price':
            value = 'Precio maximo: ' + utils.prettyPrice(pk_value)
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'gpu_brand':
            value = 'Tarjetas de video ' + unicode(VideoCardGpuBrand.objects.get(pk = pk_value))
        if key == 'gpu_family':
            value = 'Tarjetas de video ' + unicode(VideoCardGpuFamily.objects.get(pk = pk_value))
        if key == 'brand':
            value = 'Tarjetas de video ' + unicode(VideoCardBrand.objects.get(pk = pk_value))
        if key == 'gpu_line':
            value = 'Tarjetas de video ' + unicode(VideoCardGpuLine.objects.get(pk = pk_value))
        if key == 'gpu':
            value = 'Tarjetas de video ' + unicode(VideoCardGpu.objects.get(pk = pk_value))
        if key == 'gpu_core_count':
            value = 'Tarjetas de video ' + unicode(VideoCardGpuCoreCount.objects.get(pk = pk_value))
        if key == 'memory_quantity':
            value = 'Tarjetas de video con ' + unicode(VideoCardMemoryQuantity.objects.get(pk = pk_value)) + ' de memoria'
        if key == 'memory_type':
            value = 'Tarjetas de video con memoria ' + unicode(VideoCardMemoryType.objects.get(pk = pk_value))
        if key == 'memory_bus_width':
            value = 'Tarjetas de video con memorias de ' + unicode(VideoCardMemoryBusWidth.objects.get(pk = pk_value))
        if key == 'gpu_architecture':
            value = 'Tarjetas de video ' + unicode(VideoCardGpuArchitecture.objects.get(pk = pk_value))
        if key == 'gpu_core_family':
            value = 'Tarjetas de video con núcleo ' + unicode(VideoCardGpuCoreFamily.objects.get(pk = pk_value))
        if key == 'gpu_dx_version':
            value = 'Tarjetas de video DirectX ' + unicode(VideoCardGpuDirecxVersion.objects.get(pk = pk_value))
        if key == 'gpu_ogl_version':
            value = 'Tarjetas de video OpenGL ' + unicode(VideoCardGpuOpenglVersion.objects.get(pk = pk_value))
        if key == 'bus_name':
            value = 'Tarjetas de video con bus ' + unicode(VideoCardBusName.objects.get(pk = pk_value))
        if key == 'bus_lanes':
            value = 'Tarjetas de video con bus de ' + unicode(VideoCardBusLane.objects.get(pk = pk_value)) + ' lanes'
        if key == 'bus':
            value = 'Tarjetas de video con bus ' + unicode(VideoCardBus.objects.get(pk = pk_value))
        if key == 'profile':
            value = 'Tarjetas de video ' + unicode(VideoCardProfile.objects.get(pk = pk_value))
        if key == 'refrigeration':
            value = 'Tarjetas de video con refrigeración ' + unicode(VideoCardRefrigeration.objects.get(pk = pk_value))
        if key == 'slots':
            value = 'Tarjetas de video ' + unicode(VideoCardSlotType.objects.get(pk = pk_value))
        if key == 'min_price':
            value = 'Tarjetas de video con precio mínimo de ' + utils.prettyPrice(pk_value)
        if key == 'max_price':
            value = 'Tarjetas de video con precio máximo de ' + utils.prettyPrice(pk_value)
        return value  
        
    def filter_products(self, video_cards):
        if self.gpu_brand:
            video_cards = video_cards.filter(gpu__line__family__brand = self.gpu_brand)
        if self.gpu_family:
            video_cards = video_cards.filter(gpu__line__family = self.gpu_family)
        if self.brand and self.advanced_controls:
            video_cards = video_cards.filter(brand = self.brand)
        if self.gpu_line:
            video_cards = video_cards.filter(gpu__line = self.gpu_line)
        if self.gpu:
            video_cards = video_cards.filter(gpu = self.gpu)
        if self.gpu_core_count and self.advanced_controls:
            video_cards = video_cards.filter(gpu__core_count = self.gpu_core_count)
        if self.memory_quantity:
            video_cards = video_cards.filter(memory_quantity = self.memory_quantity)
        if self.memory_type and self.advanced_controls:
            video_cards = video_cards.filter(memory_type = self.memory_type)
        if self.memory_bus_width and self.advanced_controls:
            video_cards = video_cards.filter(memory_bus_width = self.memory_bus_width)
        if self.gpu_architecture:
            video_cards = video_cards.filter(gpu__core__family__architecture = self.gpu_architecture)
        if self.gpu_core_family:
            video_cards = video_cards.filter(gpu__core__family = self.gpu_core_family)
        if self.gpu_dx_version and self.advanced_controls:
            video_cards = video_cards.filter(gpu__directx_version = self.gpu_dx_version)
        if self.gpu_ogl_version and self.advanced_controls:
            video_cards = video_cards.filter(gpu__opengl_version = self.gpu_ogl_version)
        if self.bus_name:
            video_cards = video_cards.filter(bus__name = self.bus_name)
        if self.bus_lanes and self.advanced_controls:
            video_cards = video_cards.filter(bus__lanes = self.bus_lanes)
        if self.bus and self.advanced_controls:
            video_cards = video_cards.filter(bus = self.bus)
        if self.profile:
            video_cards = video_cards.filter(profile = self.profile)
        if self.refrigeration and self.advanced_controls:
            video_cards = video_cards.filter(refrigeration = self.refrigeration)
        if self.slots and self.advanced_controls:
            video_cards = video_cards.filter(slots = self.slots)
        if self.min_price:
            video_cards = video_cards.filter(min_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            video_cards = video_cards.filter(min_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            video_cards = video_cards.order_by(ordering_direction + 'min_price')
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = '-'    
            video_cards = video_cards.order_by(ordering_direction + 'gpu__tdmark_06_score')
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = '-'    
            video_cards = video_cards.order_by(ordering_direction + 'gpu__tdmark_vantage_score')
        elif self.ordering == 4:
            if ordering_direction == None:
                ordering_direction = '-'    
            video_cards = video_cards.order_by(ordering_direction + 'gpu__tdmark_11_score')
        elif self.ordering == 5:
            if ordering_direction == None:
                ordering_direction = '-'    
            video_cards = video_cards.order_by(ordering_direction + 'memory_quantity')
        else:
            if ordering_direction == None:
                ordering_direction = ''    
            video_cards = video_cards.order_by(ordering_direction + 'gpu__tdp')
            
        return video_cards
