#-*- coding: UTF-8 -*-
from django import forms
from django.db.models import Count
from solonotebooks.cotizador.models.power_supply_brand import PowerSupplyBrand
from solonotebooks.cotizador.models.power_supply_certification import PowerSupplyCertification
from solonotebooks.cotizador.models.power_supply_line import PowerSupplyLine
from solonotebooks.cotizador.models.power_supply_power import PowerSupplyPower
from solonotebooks.cotizador.models.power_supply_size import PowerSupplySize
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from . import SearchForm

class PowerSupplySearchForm(SearchForm):
    brand = ClassChoiceField(PowerSupplyBrand, 'Marca')
    line = ClassChoiceField(PowerSupplyLine, u'Línea')
    power = ClassChoiceField(PowerSupplyPower, 'Potencia')
    certification = ClassChoiceField(PowerSupplyCertification, u'Certif.')
    size = ClassChoiceField(PowerSupplySize, u'Tamaño', requires_advanced_controls=True)

    boolean_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    is_modular = CustomChoiceField(choices = boolean_choices).set_name('Modular').does_require_advanced_controls()
    has_active_pfc = CustomChoiceField(choices = boolean_choices).set_name('PFC act.').does_require_advanced_controls()

    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Potencia'),
        ('3', 'Certificación'),
    )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 150000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = \
            [
                ['Datos generales',
                    ['brand',
                     'line']],
                ['Especificaciones',
                    ['power',
                     'certification',
                     'size',
                     'is_modular',
                     'has_active_pfc',
                     ]
                ],
            ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'certification'

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(PowerSupplyBrand.objects.get(pk=pk_value))
        elif key == 'line':
            value = unicode(PowerSupplyLine.objects.get(pk=pk_value))
        elif key == 'power':
            value = u'Potencia mínima de ' + unicode(PowerSupplyPower.objects.get(pk=pk_value))
        elif key == 'certification':
            value = u'Certificación mínima: ' + unicode(PowerSupplyCertification.objects.get(pk=pk_value))
        elif key == 'size':
            value = u'Tamaño ' + unicode(PowerSupplyLine.objects.get(pk=pk_value))
        elif key == 'is_modular':
            value = ['No modular', 'Modular'][pk_value - 1]
        elif key == 'has_active_pfc':
            value = ['Sin', 'Con'][pk_value - 1] + u' PFC activo'
        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Fuentes de poder ' + unicode(PowerSupplyBrand.objects.get(pk=pk_value))
        elif key == 'line':
            value = 'Fuentes de poder ' + unicode(PowerSupplyLine.objects.get(pk=pk_value))
        elif key == 'power':
            value = u'Fuentes de poder con potencia mínima de ' + unicode(PowerSupplyPower.objects.get(pk=pk_value))
        elif key == 'certification':
            value = u'Fuentes de poder con certificación mínima ' + unicode(PowerSupplyCertification.objects.get(pk=pk_value))
        elif key == 'size':
            value = u'Fuentes de poder de tamaño ' + unicode(PowerSupplyLine.objects.get(pk=pk_value))
        elif key == 'is_modular':
            value = 'Fuentes de poder ' + ['no modulares', 'modulares'][pk_value - 1]
        elif key == 'has_active_pfc':
            value = 'Fuentes de poder ' + ['sin', 'con'][pk_value - 1] + u' PFC activo'
        return value
        
    def filter_products(self, power_supplies):
        if self.brand:
            power_supplies = power_supplies.filter(line__brand = self.brand)
        if self.line:
            power_supplies = power_supplies.filter(line = self.line)
        if self.power:
            power_supplies = power_supplies.filter(power__value__gte = PowerSupplyPower.objects.get(pk=self.power).value)
        if self.certification:
            power_supplies = power_supplies.filter(certification__value__gte = PowerSupplyCertification.objects.get(pk=self.certification).value)
        if self.size and self.advanced_controls:
            power_supplies = power_supplies.filter(size = self.size)
        if self.is_modular and self.advanced_controls:
            power_supplies = power_supplies.filter(is_modular = self.is_modular - 1)
        if self.has_active_pfc and self.advanced_controls:
            power_supplies = power_supplies.filter(has_active_pfc = self.has_active_pfc - 1)

        if self.min_price:
            power_supplies = power_supplies.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            power_supplies = power_supplies.filter(shp__shpe__latest_price__lte = int(self.max_price))

        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction is None:
                ordering_direction = ''
            power_supplies = power_supplies.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction is None:
                ordering_direction = '-'
            power_supplies = power_supplies.order_by(ordering_direction + 'power')
        elif self.ordering == 3:
            if ordering_direction is None:
                ordering_direction = '-'
            power_supplies = power_supplies.order_by(ordering_direction + 'certification')
        else:
            power_supplies = self.handle_extra_ordering(power_supplies)
            
        return power_supplies