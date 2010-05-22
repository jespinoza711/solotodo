#-*- coding: UTF-8 -*-
# Class that represents the search form to find notebooks
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils

class SearchForm(forms.Form):
    notebook_brand = forms.ModelChoiceField(NotebookBrand.objects.all(),
                                        empty_label="Cualquiera")
    notebook_line = forms.ModelChoiceField(NotebookLine.objects.all(),
                                        empty_label="Cualquiera")
    weight = forms.ChoiceField(choices=(('', 'Cualquiera'), ('0', '< 1 kg'), ('1', '1 - 2 kg'), ('2', '2 - 3 kg'), ('3', '3 - 4 kg'), ('4', '> 4 kg')))
    ordering = forms.ChoiceField(choices=(('1', 'Precio'), ('2', 'Velocidad del procesador'), ('3', 'Velocidad de la tarjeta de video'), ('4', 'Cantidad de RAM'),
    ('5', 'Capacidad de almacenamiento'), ('6', 'Peso')))
    ordering_direction = forms.IntegerField(widget=forms.HiddenInput())
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
    # These two are disabled in the HTML rendering because there is a slider
    min_price = forms.IntegerField(widget = forms.TextInput(attrs = {'class': 'price_range_input', 'disabled':'disabled'}))
    max_price = forms.IntegerField(widget = forms.TextInput(attrs = {'class': 'price_range_input', 'disabled':'disabled'}))
        
    page_number = forms.IntegerField()
    
    # These attributes are used only when querying with advanced filters
    attribute_requiring_advanced_controls = ['notebook_line',
        'weight', 'min_price', 'max_price', 'processor_line', 'processor',
        'processor_family', 'ram_type', 'ram_frequency', 'storage_type',
        'screen_size', 'screen_resolution', 'screen_touch', 'video_card_brand',
        'video_card_line', 'video_card', 'chipset']
        
    '''Generate the GET request (?var1=val1&var2=val2...) of the current query, 
    allowing to skip some of the keys if necessary (for example, when creating
    the link to the next and previous page, we need to delete the current 
    "page_number")'''
    def generateCurrentUrlWithSkip(self, skip_keys):
        url = '?'
        for key in self.data.keys():
            if not self.data[key] or key in skip_keys:
                continue
            url += key + '=' + str(self.data[key]) + '&'
        return url
        
    '''Simple method used to create the base link called when the user changes
    the sorting criteria (for example, from weight to price), in these cases we
    opt to also reset the ordering direction, as each ordering criteria has
    sensible defaults (price from low to high, CPU performance from high to
    low, etc). The result from this method is manually concatenated in the 
    template'''
    def generateUrlWithoutOrdering(self):
        return self.generateCurrentUrlWithSkip(['page_number', 'ordering', 'ordering_direction']) + 'ordering='
    
    '''Simple method used to create the base link when the user changes the 
    ordering direction (from ascending to descending or vicecersa), we only
    need to take away the ordering_direction'''
    def generateUrlWithoutOrderingDirection(self):
        return self.generateCurrentUrlWithSkip(['page_number', 'ordering_direction']) + 'ordering_direction='
    
    '''Simple method used to generate the base links to the other pages of the 
    query results'''
    def generateBasePageLink(self):
        return self.generateCurrentUrlWithSkip(['page_number']) + 'page_number='
        
    '''When the user selects filters and sees the query, the system shows him
    the active filters and links to removing them one by one, this method
    generates all those links for each of the active filters as a dictionary
    that binds a message (e.g.: Marca procesador: AMD) to a url that removes
    that criteria from the current list of filters'''
    def generateRemoveFilterLinks(self):
        filters = {}
        # For each filter (including those not active, represented by empty)
        for key in self.data.keys():
            # We are going to skip the special "filters" as they don't apply
            skip_keys = ['page_number', 'advanced_controls', 'ordering', 'ordering_direction']
            if key in skip_keys:
                continue
                
            # If this filter requires advanced controls, but they are not activated, skip
            if not ('advanced_controls' in self.data and self.data['advanced_controls'] and int(self.data['advanced_controls'])) and key in self.attribute_requiring_advanced_controls:
                continue
                
            # If the query includes a min/max price, we only show the link to
            # remove it if it is not the default min/max price
            min_price = Notebook.objects.filter(is_available = True).aggregate(Min('min_price'))['min_price__min']
            max_price = Notebook.objects.filter(is_available = True).aggregate(Max('min_price'))['min_price__max']
            if key == 'min_price' and int(self.data[key]) == utils.roundToFloor10000(min_price):
                continue
            if key == 'max_price' and int(self.data[key]) == utils.roundToCeil10000(max_price):
                continue
    
            # If the filter is active (i.e., its value is not empty)...
            if self.data[key]:
                # Create its matching string and link and add it to the list
                filters[self.getKeyDataValue(key, self.data[key])] = self.generateCurrentUrlWithSkip([key])
        return filters
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
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
        if key == 'weight':
            val = int(pk_value)
            if val == 0:
                value = 'Peso menor a 1 kg.'
            elif val == 4:
                value = 'Peso mayor a 4 kg.'
            else:
                value = 'Peso entre ' + str(val) + ' y ' + str(val + 1) + ' kg.'
        if key == 'min_price':
            value = 'Precio minimo: ' + utils.prettyPrice(int(pk_value))
        if key == 'max_price':
            value = 'Precio maximo: ' + utils.prettyPrice(int(pk_value))
        return value        
