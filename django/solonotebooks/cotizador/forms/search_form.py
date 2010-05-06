#-*- coding: UTF-8 -*-

from django import forms
from solonotebooks.cotizador.models import *

class SearchForm(forms.Form):
    notebook_brand = forms.ModelChoiceField(NotebookBrand.objects.all(),
                                        empty_label="Cualquiera")
    notebook_line = forms.ModelChoiceField(NotebookLine.objects.all(),
                                        empty_label="Cualquiera")
    processor_brand = forms.ModelChoiceField(ProcessorBrand.objects.all(),
                                        empty_label="Cualquiera")
    processor_line = forms.ModelChoiceField(ProcessorLine.objects.all(),
                                        empty_label="Cualquiera")
    processor_line_family = forms.ModelChoiceField(ProcessorLineFamily.objects.all(),
                                        empty_label="Cualquiera")
    processor_family = forms.ModelChoiceField(ProcessorFamily.objects.all(),
                                        empty_label="Cualquiera")
    processor = forms.ModelChoiceField(   Processor.objects.all(),
                                        empty_label="Cualquiera")
    chipset = forms.ModelChoiceField(   Chipset.objects.all(),
                                        empty_label="Cualquiera")
    ram_quantity = forms.ModelChoiceField(RamQuantity.objects.all(),
                                        empty_label="Cualquiera")
    ram_frequency = forms.ModelChoiceField(RamFrequency.objects.all(),
                                        empty_label="Cualquiera")
    ram_type = forms.ModelChoiceField(   RamType.objects.all(),
                                        empty_label="Cualquiera")
    storage_type = forms.ModelChoiceField(StorageDriveType.objects.all(),
                                        empty_label="Cualquiera")
    storage_capacity = forms.ModelChoiceField(StorageDriveCapacity.objects.all(),
                                        empty_label="Cualquiera")
    screen_size = forms.ModelChoiceField(ScreenSize.objects.all(),
                                        empty_label="Cualquiera")
    screen_size_family = forms.ModelChoiceField(ScreenSizeFamily.objects.all(), 
                                        empty_label="Cualquiera")
    screen_resolution = forms.ModelChoiceField(ScreenResolution.objects.all(),
                                        empty_label="Cualquiera")
    screen_touch = forms.ChoiceField(choices=(('', 'Cualquiera'), ('0', 'No'), ('1', 'Sí')))
    operating_system = forms.ModelChoiceField(OperatingSystemFamily.objects.all(),
                                        empty_label="Cualquiera")
    video_card_brand = forms.ModelChoiceField(VideoCardBrand.objects.all(),
                                        empty_label="Cualquiera")
    video_card_line = forms.ModelChoiceField(VideoCardLine.objects.all(),
                                        empty_label="Cualquiera")
    video_card_type = forms.ModelChoiceField(VideoCardType.objects.all(),
                                        empty_label="Cualquiera")
    video_card = forms.ModelChoiceField(VideoCard.objects.all(),
                                        empty_label="Cualquiera")
    advanced_controls = forms.IntegerField()
    page_number = forms.IntegerField()
    
    def generateBasePageLink(self):
        url = '?'
        for key in self.data.keys():
            if key == 'page_number':
                continue
            url += key + '=' + self.data[key] + '&'
        url += 'page_number='
        return url
        
    def generateRemoveFilterLinks(self):
        filters = {}
        for key in self.data.keys():
            if key == 'page_number' or key == 'advanced_controls':
                continue
            if self.data[key]:
                filters[self.getKeyDataValue(key, self.data[key])] = self.generateLinkExcluding(key)
        return filters
        
    def getKeyDataValue(self, key, pk_value):
        value = ''
        if key == 'notebook_brand':
            value = 'Marca: ' + unicode(NotebookBrand.objects.get(pk = pk_value))
        if key == 'notebook_line':
            value = 'Linea: ' + unicode(NotebookLine.objects.get(pk = pk_value))
        if key == 'processor_brand':
            value = 'Marca procesador: ' + unicode(ProcessorBrand.objects.get(pk = pk_value))
        if key == 'processor_line':
            value = 'Linea esp. procesador: ' + unicode(ProcessorLine.objects.get(pk = pk_value))
        if key == 'processor_line_family':
            value = 'Linea procesador: ' + unicode(ProcessorLineFamily.objects.get(pk = pk_value))
        if key == 'processor_family':
            value = 'Familia procesador: ' + unicode(ProcessorFamily.objects.get(pk = pk_value))
        if key == 'processor':
            value = 'Processor: ' + unicode(Processor.objects.get(pk = pk_value))
        if key == 'chipset':
            value = 'Chipset: ' + unicode(Chipset.objects.get(pk = pk_value))
        if key == 'ram_quantity':
            value = 'Cantidad RAM: ' + unicode(RamQuantity.objects.get(pk = pk_value))
        if key == 'ram_frequency':
            value = 'Frecuencia RAM: ' + unicode(RamFrequency.objects.get(pk = pk_value))
        if key == 'ram_type':
            value = 'Tipo RAM: ' + unicode(RamType.objects.get(pk = pk_value))
        if key == 'storage_type':
            value = 'Tipo almacenamiento: ' + unicode(StorageDriveType.objects.get(pk = pk_value))
        if key == 'storage_capacity':
            value = 'Capacidad almacenamiento: ' + unicode(StorageDriveCapacity.objects.get(pk = pk_value))
        if key == 'screen_size':
            value = 'Tamano esp. pantalla: ' + unicode(ScreenSize.objects.get(pk = pk_value))
        if key == 'screen_size_family':
            value = 'Tamano pantalla: ' + unicode(ScreenSizeFamily.objects.get(pk = pk_value))                
        if key == 'screen_resolution':
            value = 'Resolucion pantalla: ' + unicode(ScreenResolution.objects.get(pk = pk_value))
        if key == 'operating_system':
            value = 'Sistema operativo: ' + unicode(OperatingSystemFamily.objects.get(pk = pk_value))
        if key == 'video_card_brand':
            value = 'Marca tarjeta de video: ' + unicode(VideoCardBrand.objects.get(pk = pk_value))
        if key == 'video_card_line':
            value = 'Linea tarjeta de video: ' + unicode(VideoCardLine.objects.get(pk = pk_value))
        if key == 'video_card_type':
            value = 'Tipo tarjeta de video: ' + unicode(VideoCardType.objects.get(pk = pk_value))
        if key == 'video_card':
            value = 'Tarjeta de video: ' + unicode(VideoCard.objects.get(pk = pk_value))
        if key == 'screen_touch':
            value = 'Pantalla tactil: ' + ['No', 'Si'][int(pk_value)]
        return value        
        
    def generateLinkExcluding(self, skip_key):
        url = '?'
        for key in self.data.keys():
            if not self.data[key] or key == skip_key:
                continue
            url += key + '=' + self.data[key] + '&'
        return url
