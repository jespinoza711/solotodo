#-*- coding: UTF-8 -*-
from django import forms
from django.db.models import Count
from solonotebooks.cotizador.models.storage_drive_brand import StorageDriveBrand
from solonotebooks.cotizador.models.storage_drive_bus import StorageDriveBus
from solonotebooks.cotizador.models.storage_drive_capacity import StorageDriveCapacity
from solonotebooks.cotizador.models.storage_drive_family import StorageDriveFamily
from solonotebooks.cotizador.models.storage_drive_line import StorageDriveLine
from solonotebooks.cotizador.models.storage_drive_rpm import StorageDriveRpm
from solonotebooks.cotizador.models.storage_drive_size import StorageDriveSize
from solonotebooks.cotizador.models.storage_drive_type import StorageDriveType
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from . import SearchForm

class StorageDriveSearchForm(SearchForm):
    type = ClassChoiceField(StorageDriveType, 'Tipo')
    brand = ClassChoiceField(StorageDriveBrand, 'Marca')
    family = ClassChoiceField(StorageDriveFamily, 'Familia', requires_advanced_controls=True)
    line = ClassChoiceField(StorageDriveLine, 'Línea', requires_advanced_controls=True)
    capacity = ClassChoiceField(StorageDriveCapacity, 'Capacidad')
    rpm = ClassChoiceField(StorageDriveRpm, 'RPM mín.')
    size = ClassChoiceField(StorageDriveSize, 'Tamaño')
    bus = ClassChoiceField(StorageDriveBus, 'Bus', requires_advanced_controls=True)

    ordering_choices = (
        ('1', 'Precio'), 
        ('2', 'Capacidad total'),
        ('3', 'Velocidad lectura secuencial'),
    )
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
        
    price_choices = SearchForm.generate_price_range(0, 200000, 10000)
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    def generate_interface_model(self):
        model = \
            [
                ['Datos generales',
                    ['type',
                     'brand',
                     'family',
                     'line']],
                ['Especificaciones',
                    ['capacity',
                     'rpm',
                     'size',
                     'bus',
                     ]
                ],
            ]
                     
        return self.parse_model(model)
        
    def main_category_string(self):
        return 'type'

    def get_key_data_value(self, key, pk_value):
        value = ''
        if key == 'type':
            value = unicode(StorageDriveType.objects.get(pk=pk_value))
        elif key == 'brand':
            value = unicode(StorageDriveBrand.objects.get(pk=pk_value))
        elif key == 'family':
            value = unicode(StorageDriveFamily.objects.get(pk=pk_value))
        elif key == 'line':
            value = unicode(StorageDriveLine.objects.get(pk=pk_value))
        elif key == 'capacity':
            value = u'Capacidad mínima de ' + unicode(StorageDriveCapacity.objects.get(pk=pk_value))
        elif key == 'rpm':
            value = u'RPM mínimo de ' + unicode(StorageDriveRpm.objects.get(pk=pk_value))
        elif key == 'size':
            value = unicode(StorageDriveSize.objects.get(pk=pk_value))
        elif key == 'bus':
            value = unicode(StorageDriveBus.objects.get(pk=pk_value))
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generate_title_tag(self, key, pk_value):
        value = ''
        if key == 'type':
            value = 'Unidades de almacenamiento ' + unicode(StorageDriveType.objects.get(pk=pk_value))
        elif key == 'brand':
            value = 'Unidades de almacenamiento ' + unicode(StorageDriveBrand.objects.get(pk=pk_value))
        elif key == 'family':
            value = 'Unidades de almacenamiento ' + unicode(StorageDriveFamily.objects.get(pk=pk_value))
        elif key == 'line':
            value = 'Unidades de almacenamiento ' + unicode(StorageDriveLine.objects.get(pk=pk_value))
        elif key == 'capacity':
            value = u'Unidades de almacenamiento con capacidad mínima de ' + unicode(StorageDriveCapacity.objects.get(pk=pk_value))
        elif key == 'rpm':
            value = u'Unidades de almacenamiento con RPM mínimo de ' + unicode(StorageDriveRpm.objects.get(pk=pk_value))
        elif key == 'size':
            value = 'Unidades de almacenamiento de ' + unicode(StorageDriveSize.objects.get(pk=pk_value))
        elif key == 'bus':
            value = 'Unidades de almacenamiento ' + unicode(StorageDriveBus.objects.get(pk=pk_value))
        return value
        
    def filter_products(self, storage_drives):
        if self.type:
            storage_drives = storage_drives.filter(type = self.type)
        if self.brand:
            storage_drives = storage_drives.filter(line__family__brand = self.brand)
        if self.family and self.advanced_controls:
            storage_drives = storage_drives.filter(line__family = self.family)
        if self.line and self.advanced_controls:
            storage_drives = storage_drives.filter(line = self.line)
        if self.capacity:
            storage_drives = storage_drives.filter(capacity__value__gte = StorageDriveCapacity.objects.get(pk=self.capacity).value)
        if self.rpm:
            storage_drives = storage_drives.filter(rpm__value__gte = StorageDriveRpm.objects.get(pk=self.rpm).value)
        if self.size:
            storage_drives = storage_drives.filter(size = self.size)
        if self.bus and self.advanced_controls:
            storage_drives = storage_drives.filter(bus = self.bus)

        if self.min_price:
            storage_drives = storage_drives.filter(shp__shpe__latest_price__gte = int(self.min_price))
        if self.max_price and self.max_price != int(self.price_choices[-1][0]):
            storage_drives = storage_drives.filter(shp__shpe__latest_price__lte = int(self.max_price))
            
        # Check the ordering orientation, if it is not set, each criteria uses 
        # sensible defaults (asc for price, desc for cpu performance, etc)
        ordering_direction = [None, '', '-'][self.ordering_direction]
        
        # Apply the corresponding ordering based on the key
        if self.ordering == 1:
            if ordering_direction is None:
                ordering_direction = ''
            storage_drives = storage_drives.annotate(null_position=Count('shp')).order_by('-null_position', ordering_direction + 'shp__shpe__latest_price')
        elif self.ordering == 2:
            if ordering_direction is None:
                ordering_direction = '-'
            storage_drives = storage_drives.order_by(ordering_direction + 'capacity__value')
        elif self.ordering == 3:
            if ordering_direction is None:
                ordering_direction = '-'
            storage_drives = storage_drives.order_by(ordering_direction + 'sequential_read_speed')
        else:
            storage_drives = self.handle_extra_ordering(storage_drives)
            
        return storage_drives