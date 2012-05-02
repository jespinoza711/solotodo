#-*- coding: UTF-8 -*-
from django import forms
from django.db.models import Count
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from . import SearchForm

class ComputerCaseSearchForm(SearchForm):
    brand = ClassChoiceField(ComputerCaseBrand, 'Marca')
    motherboard_format = ClassChoiceField(ComputerCaseMotherboardFormat, 'Formato')
    power_supply = ClassChoiceField(ComputerCasePowerSupply, 'PSU')
    power_supply_position = ClassChoiceField(ComputerCasePowerSupplyPosition, 'Ubi. PSU')

    motherboard_tray_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    motherboard_tray = CustomChoiceField(choices=motherboard_tray_choices).set_name('Bandeja')

    ordering_choices = (
        ('1', 'Precio'),
        ('2', 'Peso'),
        ('3', 'Tamaño'),
        )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget=forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 150000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['brand',
                     'motherboard_format',
                     'power_supply',
                     'power_supply_position',
                     'motherboard_tray'
                     ]],
                     ]      
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'motherboard_format'

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(ComputerCaseBrand.objects.get(pk = pk_value))
        if key == 'power_supply':
            psu = ComputerCasePowerSupply.objects.get(pk = pk_value)
            if psu.power:
                value = u'Fuente de poder mínima: ' + unicode(psu)
            else:
                value = 'Sin fuente de poder'
        if key == 'motherboard_format':
            value = 'Formato: ' + unicode(ComputerCaseMotherboardFormat.objects.get(pk = pk_value))
        if key == 'power_supply_position':
            value = u'Posición PSU: ' + unicode(ComputerCasePowerSupplyPosition.objects.get(pk = pk_value))
        if key == 'motherboard_tray':
            value = ('Sin', 'Con')[pk_value - 1] + ' bandeja para placa madre removible'

        return value
        
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'Gabinetes ' + unicode(ComputerCaseBrand.objects.get(pk = pk_value))
        if key == 'power_supply':
            psu = ComputerCasePowerSupply.objects.get(pk = pk_value)
            if psu.power:
                value = u'Gabinetes con fuente de poder mínima de ' + unicode(psu)
            else:
                value = 'Gabinetes sin fuente de poder'
        if key == 'motherboard_format':
            value = 'Gabinetes ' + unicode(ComputerCaseMotherboardFormat.objects.get(pk = pk_value))
        if key == 'power_supply_position':
            value = 'Gabinetes con fuente de poder ' + unicode(ComputerCasePowerSupplyPosition.objects.get(pk = pk_value))
        if key == 'motherboard_tray':
            value = 'Gabinetes ' + ('sin', 'con')[pk_value - 1] + ' bandeja para placa madre removible'
        return value
        
    def filter_products(self, computer_cases):
        if self.brand:
            computer_cases = computer_cases.filter(brand = self.brand)
        if self.power_supply:
            psu = ComputerCasePowerSupply.objects.get(pk=self.power_supply)
            if psu.power:
                computer_cases = computer_cases.filter(power_supply__power__gte=psu.power)
            else:
                computer_cases = computer_cases.filter(power_supply=psu)
        if self.motherboard_format:
            computer_cases = computer_cases.filter(largest_motherboard_format=self.motherboard_format)
        if self.power_supply_position:
            computer_cases = computer_cases.filter(power_supply_position=self.power_supply_position)
        if self.motherboard_tray:
            computer_cases = computer_cases.filter(has_motherboard_tray=self.motherboard_tray-1)

        if self.min_price:
            computer_cases = computer_cases.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            computer_cases = computer_cases.filter(shp__shpe__latest_price__lte = int(self.max_price))
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            computer_cases = computer_cases.annotate(null_position=Count('shp')).order_by('-null_position', 'shp__shpe__latest_price')
        elif self.ordering == 2:
            computer_cases = computer_cases.filter(weight__gt=0).order_by('weight')
        elif self.ordering == 3:
            computer_cases = computer_cases.filter(width__gt=0).extra(select={'size': 'width*length*height'}).order_by('size')
        else:
            computer_cases = self.handle_extra_ordering(computer_cases)
            
        return computer_cases
