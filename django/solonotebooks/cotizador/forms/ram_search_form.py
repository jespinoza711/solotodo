#-*- coding: UTF-8 -*-
from django import forms
from django.db.models import Count
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from . import SearchForm

class RamSearchForm(SearchForm):
    brand = ClassChoiceField(RamBrand, 'Marca', in_quick_search=True, quick_search_name='Marca')
    line = ClassChoiceField(RamLine, 'Línea', requires_advanced_controls=True)
    total_capacity = ClassChoiceField(RamTotalCapacity, u'Cap. total', in_quick_search=True, quick_search_name='Capacidad')
    capacity = ClassChoiceField(RamCapacity, 'Cap. esp.')
    type = ClassChoiceField(InterfaceMemoryType, 'Tipo', in_quick_search=True, quick_search_name='Tipo')
    format = ClassChoiceField(InterfaceMemoryFormat, 'Formato', in_quick_search=True, quick_search_name='Formato')
    frequency = ClassChoiceField(RamFrequency, u'Frec. mín')
    voltage = ClassChoiceField(RamVoltage, u'Volt. máx', requires_advanced_controls=True)
    latency_cl = ClassChoiceField(RamLatencyCl, 'Cl (CAS)')
    latency_trcd = ClassChoiceField(RamLatencyTrcd, 'Trcd', requires_advanced_controls=True)
    latency_trp = ClassChoiceField(RamLatencyTrp, 'Trp', requires_advanced_controls=True)
    latency_tras = ClassChoiceField(RamLatencyTras, 'Tras', requires_advanced_controls=True)

    is_ecc_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    is_ecc = CustomChoiceField(choices = is_ecc_choices).set_name('ECC').does_require_advanced_controls()

    is_fully_buffered_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    is_fully_buffered = CustomChoiceField(choices = is_fully_buffered_choices).set_name('Fully buff.').does_require_advanced_controls()
    
    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Capacidad total'),
        ('3', 'Frecuencia'),
        ('4', 'Latencia Cl (CAS)'),
    )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 200000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = [['Datos generales',
                    ['brand',
                     'line',
                     'total_capacity',
                     'capacity']],
                 ['Especificaciones',
                    ['type',
                     'format',
                     'frequency',
                     'voltage',
                     ]],
                 ['Avanzado',
                    ['latency_cl',
                     'latency_trcd',
                     'latency_trp',
                     'latency_tras',
                     'is_ecc',
                     'is_fully_buffered'
                    ]],
                     ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'type'

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = unicode(RamBrand.objects.get(pk=pk_value))
        elif key == 'line':
            value = unicode(RamLine.objects.get(pk=pk_value))
        elif key == 'total_capacity':
            value = u'Capacidad mínima de ' + unicode(RamTotalCapacity.objects.get(pk=pk_value))
        elif key == 'capacity':
            value = u'Capacidad de ' + unicode(RamCapacity.objects.get(pk=pk_value))
        elif key == 'type':
            value = unicode(InterfaceMemoryType.objects.get(pk=pk_value))
        elif key == 'format':
            value = 'Formato ' + unicode(InterfaceMemoryFormat.objects.get(pk=pk_value))
        elif key == 'frequency':
            value = u'Frecuencia mínima de ' + unicode(RamFrequency.objects.get(pk=pk_value))
        elif key == 'voltage':
            value = u'Voltaje máximo de ' + unicode(RamVoltage.objects.get(pk=pk_value))
        elif key == 'latency_cl':
            value = u'Latencia Cl (CAS) máxima: ' + unicode(RamLatencyCl.objects.get(pk=pk_value))
        elif key == 'latency_trcd':
            value = u'Latencia Trcd máxima: ' + unicode(RamLatencyTrcd.objects.get(pk=pk_value))
        elif key == 'latency_trp':
            value = u'Latencia Trp máxima: ' + unicode(RamLatencyTrp.objects.get(pk=pk_value))
        elif key == 'latency_tras':
            value = u'Latencia Tras máxima: ' + unicode(RamLatencyTras.objects.get(pk=pk_value))
        elif key == 'is_ecc':
            value = ['Sin', 'Con'][pk_value - 1] + ' soporte ECC'
        elif key == 'is_fully_buffered':
            value = ['Sin', 'Con'][pk_value - 1] + ' soporte de full buffer'
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'brand':
            value = 'RAM ' + unicode(RamBrand.objects.get(pk = pk_value))
        elif key == 'line':
            value = 'RAM ' + unicode(RamLine.objects.get(pk = pk_value))
        elif key == 'total_capacity':
            value = u'RAM con capacidad mínima de ' + unicode(RamTotalCapacity.objects.get(pk = pk_value))
        elif key == 'capacity':
            value = 'RAM con capacidad de ' + unicode(RamCapacity.objects.get(pk = pk_value))
        elif key == 'type':
            value = 'RAM ' + unicode(InterfaceMemoryType.objects.get(pk = pk_value))
        elif key == 'format':
            value = 'RAM con formato ' + unicode(InterfaceMemoryFormat.objects.get(pk = pk_value))
        elif key == 'frequency':
            value = u'RAM con frecuencia mínima de ' + unicode(RamFrequency.objects.get(pk = pk_value))
        elif key == 'voltage':
            value = u'RAM con voltaje máximo de ' + unicode(RamVoltage.objects.get(pk = pk_value))
        elif key == 'latency_cl':
            value = u'RAM con latencia Cl (CAS) máxima de ' + unicode(RamLatencyCl.objects.get(pk = pk_value))
        elif key == 'latency_trcd':
            value = u'RAM con latencia Trcd máxima de ' + unicode(RamLatencyTrcd.objects.get(pk = pk_value))
        elif key == 'latency_trp':
            value = u'RAM con latencia Trp máxima de ' + unicode(RamLatencyTrp.objects.get(pk = pk_value))
        elif key == 'latency_tras':
            value = u'RAM con latencia Tras máxima de ' + unicode(RamLatencyTras.objects.get(pk = pk_value))
        elif key == 'is_ecc':
            value = 'RAM ' + ['sin', 'con'][pk_value - 1] + ' soporte ECC'
        elif key == 'is_fully_buffered':
            value = 'RAM ' + ['sin', 'con'][pk_value - 1] + ' soporte de full buffer'
        return value
        
    def filter_products(self, rams):
        if self.brand:
            rams = rams.filter(line__brand = self.brand)
        if self.line and self.advanced_controls:
            rams = rams.filter(line = self.line)
        if self.total_capacity:
            rams = rams.filter(capacity__total_capacity__value__gte = RamTotalCapacity.objects.get(pk = self.total_capacity).value)
        if self.capacity:
            rams = rams.filter(capacity = self.capacity)
        if self.type:
            rams = rams.filter(bus__bus__bus__type = self.type)
        if self.format:
            rams = rams.filter(bus__bus__bus__format = self.format)
        if self.frequency:
            rams = rams.filter(bus__frequency__value__gte = RamFrequency.objects.get(pk=self.frequency).value)
        if self.voltage and self.advanced_controls:
            rams = rams.filter(voltage__value__lte = RamVoltage.objects.get(pk=self.voltage).value)
        if self.is_ecc and self.advanced_controls:
            rams = rams.filter(is_ecc = self.is_ecc - 1)
        if self.is_fully_buffered and self.advanced_controls:
            rams = rams.filter(is_fully_buffered = self.is_fully_buffered - 1)
        if self.latency_cl:
            rams = rams.filter(latency_cl__value__lte = RamLatencyCl.objects.get(pk=self.latency_cl).value)
        if self.latency_trcd and self.advanced_controls:
            rams = rams.filter(latency_trcd__value__lte = RamLatencyTrcd.objects.get(pk=self.latency_trcd).value)
        if self.latency_trp and self.advanced_controls:
            rams = rams.filter(latency_trp__value__lte = RamLatencyTrp.objects.get(pk=self.latency_trp).value)
        if self.latency_tras and self.advanced_controls:
            rams = rams.filter(latency_tras__value__lte = RamLatencyTras.objects.get(pk=self.latency_tras).value)

        if self.min_price:
            rams = rams.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            rams = rams.filter(shp__shpe__latest_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction is None:
                ordering_direction = ''
            rams = rams.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction is None:
                ordering_direction = '-'
            rams = rams.order_by(ordering_direction + 'capacity__total_capacity')
        elif self.ordering == 3:
            if ordering_direction is None:
                ordering_direction = '-'
            rams = rams.order_by(ordering_direction + 'bus__frequency__value')
        elif self.ordering == 4:
            if ordering_direction is None:
                ordering_direction = '-'
            rams = rams.order_by(ordering_direction + 'latency_cl')
        else:
            rams = self.handle_extra_ordering(rams)
            
        return rams
