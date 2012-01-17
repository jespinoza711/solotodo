#-*- coding: UTF-8 -*-
# Class that represents the search form to find notebooks
from django import forms
from django.db.models import Min, Max, Count
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class NotebookSearchForm(SearchForm):
    notebook_brand = ClassChoiceField(NotebookBrand, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    notebook_line = ClassChoiceField(NotebookLine, 'Línea', requires_advanced_controls = True)
    processor_brand = ClassChoiceField(NotebookProcessorBrand, 'Marca')
    processor_line_family = ClassChoiceField(NotebookProcessorLineFamily, 'Línea', in_quick_search = True, quick_search_name = 'Procesador')
    processor = ClassChoiceField(NotebookProcessor, 'Modelo', requires_advanced_controls = True)
    ram_quantity = ClassChoiceField(NotebookRamQuantity, 'Cant. min.', in_quick_search = True, quick_search_name = 'RAM')
    ram_type = ClassChoiceField(NotebookRamType, 'Tipo', requires_advanced_controls = True)
    storage_type = ClassChoiceField(NotebookStorageDriveType, 'Tipo', requires_advanced_controls = True)
    storage_capacity = ClassChoiceField(NotebookStorageDriveCapacity, 'Cant. min.')
    storage_rpm = ClassChoiceField(NotebookStorageDriveRpm, 'RPM', requires_advanced_controls = True)
    min_size, max_size = ClassChoiceField.generate_slider(NotebookScreenSizeFamily)
    screen_resolution = ClassChoiceField(NotebookScreenResolution, 'Resolución', requires_advanced_controls = True)
    operating_system = ClassChoiceField(NotebookOperatingSystemFamily, 'Nombre')
    video_card_brand = ClassChoiceField(NotebookVideoCardBrand, 'Marca', requires_advanced_controls = True)
    video_card_line = ClassChoiceField(NotebookVideoCardLine, 'Línea', requires_advanced_controls = True)
    video_card_type = ClassChoiceField(NotebookVideoCardType, 'Tipo', in_quick_search = True, quick_search_name = 'Tarjeta de video')
    video_card = ClassChoiceField(NotebookVideoCard, 'Modelo', requires_advanced_controls = True)
    
    ordering_choices = (('1', 'Precio'), ('2', 'Capacidad para correr aplicaciones'), ('3', 'Capacidad para correr juegos'),
    ('6', 'Peso'))
    screen_touch_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
    screen_touch = CustomChoiceField(choices = screen_touch_choices).set_name('Táctil').does_require_advanced_controls()
    ntype = ClassChoiceField(NotebookType, 'Uso')
        
    price_choices = SearchForm.generate_price_range(0, 800000, 50000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['notebook_brand',
                     'notebook_line']],
                 ['Procesador',
                    ['processor_brand',
                     'processor_line_family',
                     'processor']],
                 ['RAM',
                    ['ram_quantity',
                     'ram_type']],
                 ['Disco Duro',
                    ['storage_capacity',
                     'storage_type',
                     'storage_rpm']],
                 ['Pantalla',
                    ['min_size',
                     'max_size',
                     'screen_resolution',
                     'screen_touch']],
                 ['Tarjeta de video',
                    ['video_card_type',
                     'video_card_brand',
                     'video_card_line',
                     'video_card']],
                 ['Sistema operativo',
                    ['operating_system'],
                     ]]
                     
        return self.parse_model(model)
        
    def __init__(self, qd, extra_permissions):
        if 'max_size' not in qd:
            qd['max_size'] = NotebookScreenSizeFamily.objects.reverse()[0].id
        if 'min_size' not in qd:
            qd['min_size'] = NotebookScreenSizeFamily.objects.all()[0].id
        super(NotebookSearchForm, self).__init__(qd, extra_permissions)
        
    def main_category_string(self):
        return 'ntype'    

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'notebook_brand':
            value = unicode(NotebookBrand.objects.get(pk = pk_value))
        if key == 'notebook_line':
            value = unicode(NotebookLine.objects.get(pk = pk_value))
        if key == 'processor_brand':
            value = 'Procesador ' + unicode(NotebookProcessorBrand.objects.get(pk = pk_value))
        if key == 'processor_line_family':
            value = 'Procesador: ' + unicode(NotebookProcessorLineFamily.objects.get(pk = pk_value))
        if key == 'processor':
            value = 'Procesador: ' + unicode(NotebookProcessor.objects.get(pk = pk_value))
        if key == 'ram_quantity':
            value = unicode(NotebookRamQuantity.objects.get(pk = pk_value)) + u' o más de RAM'
        if key == 'ram_type':
            value = 'RAM ' + unicode(NotebookRamType.objects.get(pk = pk_value))
        if key == 'storage_type':
            value = 'Almacenamiento ' + unicode(NotebookStorageDriveType.objects.get(pk = pk_value))
        if key == 'storage_capacity':
            value = unicode(NotebookStorageDriveCapacity.objects.get(pk = pk_value)) + u' o más de almacenamiento'
        if key == 'storage_rpm':
            value = 'RPM: ' + unicode(NotebookStorageDriveRpm.objects.get(pk = pk_value))
        if key == 'min_size':
            value = u'Tamaño mínimo: ' + unicode(NotebookScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'max_size':
            value = u'Tamaño máximo: ' + unicode(NotebookScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'screen_resolution':
            value = 'Resolucion de ' + unicode(NotebookScreenResolution.objects.get(pk = pk_value))
        if key == 'operating_system':
            value = unicode(NotebookOperatingSystemFamily.objects.get(pk = pk_value))
        if key == 'video_card_brand':
            value = 'Tarjeta de video ' + unicode(NotebookVideoCardBrand.objects.get(pk = pk_value))
        if key == 'video_card_line':
            value = 'Tarjeta de video ' + unicode(NotebookVideoCardLine.objects.get(pk = pk_value))
        if key == 'video_card_type':
            value = 'Tarjeta de video ' + unicode(NotebookVideoCardType.objects.get(pk = pk_value))
        if key == 'video_card':
            value = 'Tarjeta de video ' + unicode(NotebookVideoCard.objects.get(pk = pk_value))
        if key == 'screen_touch':
            value = ['Sin', 'Con'][pk_value - 1] + ' pantalla táctil'
        if key == 'ntype':
            value = unicode(NotebookType.objects.get(pk = pk_value))
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'notebook_brand':
            value = 'Notebooks ' + unicode(NotebookBrand.objects.get(pk = pk_value))
        if key == 'notebook_line':
            value = 'Notebooks ' + unicode(NotebookLine.objects.get(pk = pk_value))
        if key == 'processor_brand':
            value = 'Notebooks con procesadores ' + unicode(NotebookProcessorBrand.objects.get(pk = pk_value))
        if key == 'processor_line_family':
            value = 'Notebooks con procesadores ' + unicode(NotebookProcessorLineFamily.objects.get(pk = pk_value))
        if key == 'processor':
            value = 'Notebooks con procesadores ' + unicode(NotebookProcessor.objects.get(pk = pk_value))
        if key == 'ram_quantity':
            value = 'Notebooks con ' + unicode(NotebookRamQuantity.objects.get(pk = pk_value)) + u' o más de RAM'
        if key == 'ram_type':
            value = 'Notebooks con memoria RAM ' + unicode(NotebookRamType.objects.get(pk = pk_value))
        if key == 'storage_type':
            value = 'Notebooks con almacenamiento de tipo ' + unicode(NotebookStorageDriveType.objects.get(pk = pk_value))
        if key == 'storage_capacity':
            value = 'Notebooks con ' + unicode(NotebookStorageDriveCapacity.objects.get(pk = pk_value)) + u' o más de almacenamiento'
        if key == 'storage_rpm':
            value = 'Notebooks con dicos duros de ' + unicode(NotebookStorageDriveRpm.objects.get(pk = pk_value))
        if key == 'min_size':
            value = u'Notebooks con tamaño mínimo de ' + unicode(NotebookScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'max_size':
            value = u'Notebooks con tamaño máximo de ' + unicode(NotebookScreenSizeFamily.objects.get(pk = pk_value))
        if key == 'screen_resolution':
            value = 'Notebooks con resolucion de ' + unicode(NotebookScreenResolution.objects.get(pk = pk_value))
        if key == 'operating_system':
            value = 'Notebooks con ' + unicode(NotebookOperatingSystemFamily.objects.get(pk = pk_value))
        if key == 'video_card_brand':
            value = 'Notebooks con tarjetas de video ' + unicode(NotebookVideoCardBrand.objects.get(pk = pk_value))
        if key == 'video_card_line':
            value = 'Notebooks con tarjetas de video ' + unicode(NotebookVideoCardLine.objects.get(pk = pk_value))
        if key == 'video_card_type':
            value = 'Notebooks con tarjetas de video ' + unicode(NotebookVideoCardType.objects.get(pk = pk_value)).lower()
        if key == 'video_card':
            value = 'Notebooks con tarjetas de video ' + unicode(NotebookVideoCard.objects.get(pk = pk_value))
        if key == 'screen_touch':
            value = 'Notebooks ' + ['sin', 'con'][pk_value - 1] + ' pantalla táctil'
        if key == 'ntype':
            value = unicode(NotebookType.objects.get(pk = pk_value))
        return value        
        
    def filter_products(self, notebooks):
        if self.ntype:
            notebooks = notebooks.filter(ntype = self.ntype)
        
        if self.notebook_brand:
            notebooks = notebooks.filter(line__brand__id = self.notebook_brand)
            
        if self.processor_brand:
            notebooks = notebooks.filter(processor__line__family__brand__id = self.processor_brand)
            
        if self.processor_line_family:
            notebooks = notebooks.filter(processor__line__family__id = self.processor_line_family)
            
        if self.ram_quantity:
            notebooks = notebooks.filter(ram_quantity__value__gte = NotebookRamQuantity.objects.get(pk = self.ram_quantity).value)
            
        if self.storage_capacity:
            notebooks = notebooks.filter(storage_drive__capacity__value__gte = NotebookStorageDriveCapacity.objects.get(pk = self.storage_capacity).value).distinct()
            
        if self.min_size:
            notebooks = notebooks.filter(screen__size__family__base_size__gte = NotebookScreenSizeFamily.objects.get(pk = self.min_size).base_size)
            
        if self.max_size:
            notebooks = notebooks.filter(screen__size__family__base_size__lte = NotebookScreenSizeFamily.objects.get(pk = self.max_size).base_size)
            
        if self.video_card_type:
            notebooks = notebooks.filter(video_card__card_type__id = self.video_card_type).distinct()
            
        if self.operating_system:
            notebooks = notebooks.filter(operating_system__family__id = self.operating_system)
            
        if self.notebook_line and self.advanced_controls:
            notebooks = notebooks.filter(line__id=self.notebook_line)
            
        if self.processor and self.advanced_controls:
            notebooks = notebooks.filter(processor__id=self.processor)
            
        if self.ram_type and self.advanced_controls:
            notebooks = notebooks.filter(ram_type__id=self.ram_type)
            
        if self.storage_type and self.advanced_controls:
            notebooks = notebooks.filter(storage_drive__drive_type__id = self.storage_type)
            
        if self.storage_rpm and self.advanced_controls:
            notebooks = notebooks.filter(storage_drive__rpm__id = self.storage_rpm)
            
        if self.screen_resolution and self.advanced_controls:
            notebooks = notebooks.filter(screen__resolution__id = self.screen_resolution)
            
        if self.screen_touch and self.advanced_controls:
            notebooks = notebooks.filter(screen__is_touchscreen = self.screen_touch - 1)    
            
        if self.video_card_brand and self.advanced_controls:
            notebooks = notebooks.filter(video_card__line__brand__id = self.video_card_brand).distinct()
            
        if self.video_card_line and self.advanced_controls:
            notebooks = notebooks.filter(video_card__line__id = self.video_card_line).distinct()
            
        if self.video_card and self.advanced_controls:
            notebooks = notebooks.filter(video_card__id = self.video_card).distinct()
            
        if self.min_price:
            notebooks = notebooks.filter(shp__shpe__latest_price__gte = int(self.min_price))

        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            notebooks = notebooks.filter(shp__shpe__latest_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            notebooks = notebooks.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = '-'    
            notebooks = notebooks.order_by(ordering_direction + 'processor__speed_score')
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = '-'    
            # Note: A notebook may have more than one video card, grab the fastest
            notebooks = notebooks.annotate(max_video_card_score=Max('video_card__speed_score')).order_by(ordering_direction + 'max_video_card_score')
        elif self.ordering == 4:
            if ordering_direction == None:
                ordering_direction = '-'    
            notebooks = notebooks.order_by(ordering_direction + 'ram_quantity__value')
        elif self.ordering == 5:
            if ordering_direction == None:
                ordering_direction = '-'    
            # Note: A notebook may have more than one SD, grab the biggest
            notebooks = notebooks.annotate(max_hard_drive_capacity=Max('storage_drive__capacity__value')).order_by(ordering_direction + 'max_hard_drive_capacity')   
        elif self.ordering == 6:
            if ordering_direction == None:
                ordering_direction = ''    
            notebooks = notebooks.order_by(ordering_direction + 'weight')     
        else:
            notebooks = self.handle_extra_ordering(notebooks)
            
        return notebooks
