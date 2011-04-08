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
    
    manufacturer = ClassChoiceField(CellphoneManufacturer, 'Marca', in_quick_search = True, quick_search_name = 'Marca')
    category = ClassChoiceField(CellphoneCategory, 'Categoría')
    form_factor = ClassChoiceField(CellphoneFormFactor, 'Estilo')
    camera = ClassChoiceField(CellphoneCamera, 'Cámara')
    keyboard = ClassChoiceField(CellphoneKeyboard, 'Teclado', requires_advanced_controls = True)
    operating_system = ClassChoiceField(CellphoneOperatingSystem, 'Sist. Op.', requires_advanced_controls = True)
    
    screen_size = ClassChoiceField(CellphoneScreenSize, 'Pantalla')
    screen_touch_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    screen_touch = CustomChoiceField(choices = screen_touch_choices).set_name('Táctil')
    
    comm_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    has_3g = CustomChoiceField(choices = comm_choices).set_name('3G')
    has_bluetooth = CustomChoiceField(choices = comm_choices).set_name('Bluetooth')
    has_wifi = CustomChoiceField(choices = comm_choices).set_name('WiFi').does_require_advanced_controls()
    has_gps = CustomChoiceField(choices = comm_choices).set_name('GPS').does_require_advanced_controls()
    
    ram = ClassChoiceField(CellphoneRam, 'RAM')
    processor = ClassChoiceField(CellphoneProcessor, 'Procesador', requires_advanced_controls = True)
    graphics = ClassChoiceField(CellphoneGraphics, 'Gráficos', requires_advanced_controls = True)
    
    ordering_choices = (
        ('1', 'Precio equipo'), 
        ('2', 'Costo proyectado a 3 meses'),
        ('3', 'Costo proyectado a 6 meses'), 
        ('4', 'Costo proyectado a 12 meses'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 250000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Información del plan',
                    ['plan_company',
                     'plan_type',
                     'plan_data',]],
                 ['Precio del plan',
                    ['plan_price_min',
                     'plan_price_max']],
                 ['Datos del celular',
                    ['manufacturer',
                     'screen_size',
                     'category',
                     'form_factor',
                     'camera',
                     'keyboard',
                     'operating_system',
                     ]],
                 ['Extras del celular',
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
        if key == 'plan_company':
            value = unicode(CellCompany.objects.get(pk = pk_value))
        if key == 'plan_type':
            value = unicode(self.plan_type_choices[pk_value][1])
        if key == 'plan_data':
            value = 'Planes ' + ['sin', 'con'][pk_value - 1] + ' datos'
        if key == 'plan_price_min':
            value = u'Planes desde ' + utils.prettyPrice(pk_value)
        if key == 'plan_price_max':
            value = u'Planes hasta ' + utils.prettyPrice(pk_value)
        if key == 'manufacturer':
            value = unicode(CellphoneManufacturer.objects.get(pk = pk_value))
        if key == 'category':
            value = unicode(CellphoneCategory.objects.get(pk = pk_value))
        if key == 'form_factor':
            value = unicode(CellphoneFormFactor.objects.get(pk = pk_value))
        if key == 'camera':
            value = u'Cámara de ' + unicode(CellphoneCamera.objects.get(pk = pk_value))
        if key == 'keyboard':
            value = 'Teclado ' + unicode(CellphoneManufacturer.objects.get(pk = pk_value))
        if key == 'operating_system':
            value = 'Sistema operativo ' + unicode(CellphoneOperatingSystem.objects.get(pk = pk_value))
        if key == 'screen_size':
            value = 'Pantalla desde ' + unicode(CellphoneScreenSize.objects.get(pk = pk_value))
        if key == 'screen_touch':
            value = ['Sin', 'Con'][pk_value - 1] + u' pantalla táctil'
        if key == 'has_3g':
            value = ['Sin', 'Con'][pk_value - 1] + u' 3G'
        if key == 'has_bluetooth':
            value = ['Sin', 'Con'][pk_value - 1] + u' Bluetooth'
        if key == 'has_wifi':
            value = ['Sin', 'Con'][pk_value - 1] + u' WiFi'
        if key == 'has_gps':
            value = ['Sin', 'Con'][pk_value - 1] + u' GPS'
        if key == 'ram':
            value = 'RAM desde ' + unicode(CellphoneRam.objects.get(pk = pk_value))
        if key == 'processor':
            value = 'Procesador ' + unicode(CellphoneProcessor.objects.get(pk = pk_value))
        if key == 'graphics':
            value = u'Gráficos ' + unicode(CellphoneGraphics.objects.get(pk = pk_value))
        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'plan_company':
            value = 'Celulares con planes ' + unicode(CellCompany.objects.get(pk = pk_value))
        if key == 'plan_type':
            value = 'Celulares con planes a ' + unicode(self.plan_type_choices[pk_value][1])
        if key == 'plan_data':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + ' plan de datos'
        if key == 'plan_price_min':
            value = u'Celulares con planes desde ' + utils.prettyPrice(pk_value)
        if key == 'plan_price_max':
            value = u'Celulares con planes hasta ' + utils.prettyPrice(pk_value)
        if key == 'manufacturer':
            value = 'Celulares ' + unicode(CellphoneManufacturer.objects.get(pk = pk_value))
        if key == 'category':
            value = unicode(CellphoneCategory.objects.get(pk = pk_value))
        if key == 'form_factor':
            value = 'Celulares ' + unicode(CellphoneFormFactor.objects.get(pk = pk_value))
        if key == 'camera':
            value = u'Celulares con cámara de ' + unicode(CellphoneCamera.objects.get(pk = pk_value))
        if key == 'keyboard':
            value = 'Celulares con teclado ' + unicode(CellphoneManufacturer.objects.get(pk = pk_value))
        if key == 'operating_system':
            value = 'Celulares con sistema operativo ' + unicode(CellphoneOperatingSystem.objects.get(pk = pk_value))
        if key == 'screen_size':
            value = 'Celulares con pantalla desde ' + unicode(CellphoneScreenSize.objects.get(pk = pk_value))
        if key == 'screen_touch':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + u' pantalla táctil'
        if key == 'has_3g':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + u' 3G'
        if key == 'has_bluetooth':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + u' Bluetooth'
        if key == 'has_wifi':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + + u' WiFi'
        if key == 'has_gps':
            value = 'Celulares ' + ['sin', 'con'][pk_value - 1] + u' GPS'
        if key == 'ram':
            value = 'Celulares con RAM desde ' + unicode(CellphoneRam.objects.get(pk = pk_value))
        if key == 'processor':
            value = 'Celulares con procesador ' + unicode(CellphoneProcessor.objects.get(pk = pk_value))
        if key == 'graphics':
            value = 'Celulares con gráficos ' + unicode(CellphoneGraphics.objects.get(pk = pk_value))
        return value
        
    def filter_products(self, cells):
        tiers = CellPricingTier.objects.filter(pricing__cell__isnull = False)
        
        if self.plan_company:
            tiers = tiers.filter(pricing__company = self.plan_company)
        if self.plan_type:
            if self.plan_type == 1:
                tiers = tiers.filter(plan__price = 0)
            else:
                tiers = tiers.filter(plan__price__gt = 0)
        if self.plan_data:
            if self.plan_data == 1:
                tiers = tiers.filter(plan__includes_data = False)
            else:
                tiers = tiers.filter(plan__includes_data = True)
        if self.plan_price_min:
            tiers = tiers.filter(plan__price__gte = self.plan_price_min)
        if self.plan_price_max:
            max_price = int(self.plan_price_choices[-1][0])
            if self.plan_price_max != max_price:
                tiers = tiers.filter(plan__price__lte = self.plan_price_max)
        if self.manufacturer:
            tiers = tiers.filter(pricing__cell__phone__manufacturer = self.manufacturer)
        if self.category:
            tiers = tiers.filter(pricing__cell__phone__category = self.category)
        if self.form_factor:
            tiers = tiers.filter(pricing__cell__phone__form_factor = self.form_factor)
        if self.camera:
            tiers = tiers.filter(pricing__cell__phone__camera = self.camera)
        if self.keyboard and self.advanced_controls:
            tiers = tiers.filter(pricing__cell__phone__keyboard = self.keyboard)
        if self.operating_system and self.advanced_controls:
            tiers = tiers.filter(pricing__cell__phone__operating_system = self.operating_system)
        if self.screen_size:
            tiers = tiers.filter(pricing__cell__phone__screen__size__value__gte = CellphoneScreenSize.objects.get(pk = self.screen_size).value)
        if self.screen_touch:
            if self.screen_touch == 1:
                tiers = tiers.filter(pricing__cell__phone__screen__is_touch = False)
            else:
                tiers = tiers.filter(pricing__cell__phone__screen__is_touch = True)
        if self.has_3g:
            if self.has_3g == 1:
                tiers = tiers.filter(pricing__cell__phone__has_3g = False)
            else:
                tiers = tiers.filter(pricing__cell__phone__has_3g = True)
        if self.has_bluetooth:
            if self.has_bluetooth == 1:
                tiers = tiers.filter(pricing__cell__phone__has_bluetooth = False)
            else:
                tiers = tiers.filter(pricing__cell__phone__has_bluetooth = True)
        if self.has_wifi and self.advanced_controls:
            if self.has_wifi == 1:
                tiers = tiers.filter(pricing__cell__phone__has_wifi = False)
            else:
                tiers = tiers.filter(pricing__cell__phone__has_wifi = True)
        if self.has_gps and self.advanced_controls:
            if self.has_gps == 1:
                tiers = tiers.filter(pricing__cell__phone__has_gps = False)
            else:
                tiers = tiers.filter(pricing__cell__phone__has_gps = True)
        if self.ram:
            tiers = tiers.filter(pricing__cell__phone__ram__value__gte = CellphoneRam.objects.get(pk = self.ram).value)
        if self.processor and self.advanced_controls:
            tiers = tiers.filter(pricing__cell__phone__processor = self.processor)
        if self.graphics and self.advanced_controls:
            tiers = tiers.filter(pricing__cell__phone__graphics = self.graphics)
        
        if self.min_price:
            tiers = tiers.filter(cellphone_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            tiers = tiers.filter(cellphone_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction == None:
                ordering_direction = ''
            price_field = 'cellphone_price'
            tiers = tiers.order_by(ordering_direction + price_field)
        elif self.ordering == 2:
            if ordering_direction == None:
                ordering_direction = ''    
            price_field = 'three_month_pricing'
            tiers = tiers.order_by(ordering_direction + price_field)
        elif self.ordering == 3:
            if ordering_direction == None:
                ordering_direction = ''    
            price_field = 'six_month_pricing'
            tiers = tiers.order_by(ordering_direction + price_field)
        else:
            if ordering_direction == None:
                ordering_direction = ''    
            price_field = 'twelve_month_pricing'
            tiers = tiers.order_by(ordering_direction + price_field)
            
        final_cells = []
        cells = list(cells)
        
        for tier in tiers:
            cell = tier.pricing.cell

            if cell and cell in cells and cell not in final_cells:
                price = getattr(tier, price_field)
                cell.tier = tier
                cell.url_args = {'tier_id': tier.id}
                final_cells.append(cell)
            
        return final_cells
        
