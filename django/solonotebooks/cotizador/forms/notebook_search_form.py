#-*- coding: UTF-8 -*-
# Class that represents the search form to find notebooks
from django import forms
from django.db.models import Min, Max
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.models import utils
from solonotebooks.cotizador.fields import ClassChoiceField, CustomChoiceField
from datetime import date
from . import SearchForm

class NotebookSearchForm(SearchForm):
    notebook_brand = ClassChoiceField(NotebookBrand, 'Marca', in_quick_search = True)
    notebook_line = ClassChoiceField(NotebookLine, 'Línea', requires_advanced_controls = True)
    processor_brand = ClassChoiceField(NotebookProcessorBrand, 'Marca')
    processor_line_family = ClassChoiceField(NotebookProcessorLineFamily, 'Línea', in_quick_search = True)
    processor = ClassChoiceField(NotebookProcessor, 'Modelo', requires_advanced_controls = True)
    ram_quantity = ClassChoiceField(NotebookRamQuantity, 'Cant. min.', in_quick_search = True)
    ram_type = ClassChoiceField(NotebookRamType, 'Tipo', requires_advanced_controls = True)
    storage_type = ClassChoiceField(NotebookStorageDriveType, 'Tipo', requires_advanced_controls = True)
    storage_capacity = ClassChoiceField(NotebookStorageDriveCapacity, 'Cant. min.')
    screen_size_family = ClassChoiceField(NotebookScreenSizeFamily, 'Tamaño')
    screen_resolution = ClassChoiceField(NotebookScreenResolution, 'Resolución', requires_advanced_controls = True)
    operating_system = ClassChoiceField(NotebookOperatingSystemFamily, 'Nombre')
    video_card_brand = ClassChoiceField(NotebookVideoCardBrand, 'Marca', requires_advanced_controls = True)
    video_card_line = ClassChoiceField(NotebookVideoCardLine, 'Línea', requires_advanced_controls = True)
    video_card_type = ClassChoiceField(NotebookVideoCardType, 'Tipo', in_quick_search = True)
    video_card = ClassChoiceField(NotebookVideoCard, 'Modelo', requires_advanced_controls = True)
    
    ordering_choices = (('1', 'Precio'), ('2', 'Velocidad del procesador'), ('3', 'Capacidad para juegos'), ('4', 'Cantidad de RAM'),
    ('5', 'Capacidad de almacenamiento'), ('6', 'Peso'))
    screen_touch_choices = (('0', 'Cualquiera'), ('1', 'No'), ('2', 'Sí'))
    
    ordering = CustomChoiceField(choices = ordering_choices, widget = forms.HiddenInput()).set_name('Ordenamiento')
    screen_touch = CustomChoiceField(choices = screen_touch_choices).set_name('Táctil').requires_advanced_controls()
    ntype = ClassChoiceField(NotebookType, 'Uso', widget = forms.HiddenInput())
    
    ordering_direction = forms.IntegerField(widget = forms.HiddenInput())
    advanced_controls = forms.IntegerField(widget = forms.HiddenInput())
        
    price_choices = (('0', '0'),
                    ('100000', '100.000'),
                    ('150000', '150.000'),
                    ('200000', '200.000'),
                    ('250000', '250.000'),
                    ('300000', '300.000'),
                    ('350000', '350.000'),
                    ('400000', '400.000'),
                    ('450000', '450.000'),
                    ('500000', '500.000'),
                    ('550000', '550.000'),
                    ('600000', '600.000'),
                    ('650000', '650.000'),
                    ('700000', '700.000'),
                    ('750000', '750.000'),
                    ('800000', '800.000'),
                    ('850000', '850.000'),
                    ('900000', '900.000'),
                    ('950000', '950.000'),
                    ('1000000', '1.000.000+'))
    
    min_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Mínimo')
    max_price = CustomChoiceField(choices = price_choices, widget = forms.Select(attrs = {'class': 'price_range_select'})).set_name('Precio Máximo')
        
    page_number = forms.IntegerField()
    
    # These attributes are used only when querying with advanced filters
    attribute_requiring_advanced_controls = [
        'notebook_line',
        'processor',
        'ram_type', 
        'storage_type',
        'screen_resolution', 
        'screen_touch', 
        'video_card_brand',
        'video_card_line', 
        'video_card']
        
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
                     'storage_type']],
                 ['Pantalla',
                    ['screen_size_family',
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
        
    def main_category(self):
        return self.fields['ntype']
        
    def main_category_string(self):
        return 'ntype'
        
    def generateTitle(self):
        # We are going to skip the special "filters" as they don't apply
        skip_keys = ['page_number', 'advanced_controls', 'ordering', 'ordering_direction', 'min_price', 'max_price']
        valid_keys = []
        
        # For each filter (including those not active, represented by empty)
        for key in self.fields:
            if key in skip_keys:
                continue
                
            # If this filter requires advanced controls, but they are not activated, skip
            if not self.advanced_controls and key in self.attribute_requiring_advanced_controls:
                continue
    
            # If the filter is active (i.e., its value is not empty)...
            if key in self.__dict__ and self.__dict__[key]:
                valid_keys.append(key)
                
        if len(valid_keys) == 0:
            return 'Catálogo de notebooks'
        elif len(valid_keys) == 1:
            return self.generateTitleTag(valid_keys[0], self.__dict__[valid_keys[0]])
        else: 
            return 'Resultados de la búsqueda'
        
    def validate(self):
        fields = [[field_name, self.fields[field_name]] for field_name in self.fields]
    
        # First we validate the ClassChoiceFields
        class_choice_fields = filter(lambda x: isinstance(x[1], forms.ModelChoiceField), fields)
        
        for pair in class_choice_fields:
            try:
                choice_field_selection_id = int(self.data[pair[0]])
                field_selection_instance = pair[1].class_name.objects.get(pk = choice_field_selection_id)  
                self.__dict__[pair[0]] = choice_field_selection_id
            except:
                self.__dict__[pair[0]] = 0
                
        # ModelChoiceFields are a subclass of ChoiceField, so we need to remove
        # them from fields to prevent them from processing again
        
        fields = filter(lambda x: x not in class_choice_fields, fields)
        choice_fields = filter(lambda x: isinstance(x[1], forms.ChoiceField), fields)
        
        for pair in choice_fields:
            try:
                choice_field_selection = self.data[pair[0]]
                choices_dict = dict([[x[0], x[1]] for x in self.fields[pair[0]].choices])
                
                if not choice_field_selection in choices_dict:
                    choice_field_selection = 0
                
                self.__dict__[pair[0]] = int(choice_field_selection)
            except:
                self.__dict__[pair[0]] = 0
                
        integer_fields = filter(lambda x: isinstance(x[1], forms.IntegerField), fields)
        
        for pair in integer_fields:
            try:
                integer_field_value = int(self.data[pair[0]])
                self.__dict__[pair[0]] = integer_field_value
            except:
                self.__dict__[pair[0]] = 0
                
        # Particular cases
        if not self.ordering_direction in [0, 1, 2]:
            self.ordering_direction = 0
            
        if not self.advanced_controls in [0, 1]:
            self.advanced_controls = 0
            
        if self.page_number <= 0:
            self.page_number = 1
            
        if self.ordering == 0:
            self.ordering = 7
        
    def getOrderingOptions(self):
        return self.ordering_choices
    
    
    '''Generate the GET request (?var1=val1&var2=val2...) of the current query, 
    allowing to skip some of the keys if necessary (for example, when creating
    the link to the next and previous page, we need to delete the current 
    "page_number")'''
    def generateCurrentUrlWithSkip(self, skip_keys, start_symbol = '?'):
        keyvalues = []
        for key in self.fields:
            if key not in self.__dict__ or not self.__dict__[key] or key in skip_keys:
                continue
            keyvalues.append(key + '=' + str(self.__dict__[key]))
        return start_symbol + '&'.join(keyvalues)
        
    '''Simple method used to create the base link called when the user changes
    the sorting criteria (for example, from weight to price), in these cases we
    opt to also reset the ordering direction, as each ordering criteria has
    sensible defaults (price from low to high, CPU performance from high to
    low, etc). The result from this method is manually concatenated in the 
    template'''
    def generateUrlWithoutOrdering(self):
        return self.generateCurrentUrlWithSkip(['page_number', 'ordering', 'ordering_direction']) + '&ordering='
        
    def generateProdutLinkArgs(self):
        result = self.generateCurrentUrlWithSkip(['page_number', 'ordering', 'ordering_direction'])
        if result == '?':
            return ''
        return result
    
    '''Simple method used to create the base link when the user changes the 
    ordering direction (from ascending to descending or vicecersa), we only
    need to take away the ordering_direction'''
    def generateUrlWithoutOrderingDirection(self):
        return self.generateCurrentUrlWithSkip(['page_number', 'ordering_direction']) + '&ordering_direction='
        
    '''Simple method used to create the base link when the user changes the 
    notebook type without modifying the other criteria'''
    def generate_url_without_ntype(self):
        return self.generateCurrentUrlWithSkip(['page_number', 'ntype'], '') + '&'
    
    '''Simple method used to generate the base links to the other pages of the 
    query results'''
    def generateBasePageLink(self):
        return self.generateCurrentUrlWithSkip(['page_number']) + '&page_number='
        
    '''When the user selects filters and sees the query, the system shows him
    the active filters and links to removing them one by one, this method
    generates all those links for each of the active filters as a dictionary
    that binds a message (e.g.: Marca procesador: AMD) to a url that removes
    that criteria from the current list of filters'''
    def generate_remove_filter_links(self):
        filters = {}
        
        # We are going to skip the special "filters" as they don't apply
        skip_keys = ['page_number', 'ordering', 'ordering_direction', 'min_price', 'max_price', 'advanced_controls']
        
        # For each filter (including those not active, represented by empty)
        for key in self.fields:
            if key in skip_keys:
                continue
                
            # If this filter requires advanced controls, but they are not activated, skip
            if not self.advanced_controls and key in self.attribute_requiring_advanced_controls:
                continue
    
            # If the filter is active (i.e., its value is not empty)...
            if key in self.__dict__ and self.__dict__[key]:
                # Create its matching string and link and add it to the list
                filters[self.getKeyDataValue(key, self.__dict__[key])] = self.generateCurrentUrlWithSkip([key])
        return filters
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def getKeyDataValue(self, key, pk_value):
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
            value = unicode(NotebookRamQuantity.objects.get(pk = pk_value)) + ' de RAM'
        if key == 'ram_type':
            value = 'RAM ' + unicode(NotebookRamType.objects.get(pk = pk_value))
        if key == 'storage_type':
            value = 'Almacenamiento ' + unicode(NotebookStorageDriveType.objects.get(pk = pk_value))
        if key == 'storage_capacity':
            value = unicode(NotebookStorageDriveCapacity.objects.get(pk = pk_value)) + ' de almacenamiento'
        if key == 'screen_size_family':
            value = 'Pantalla de ' + unicode(NotebookScreenSizeFamily.objects.get(pk = pk_value))                
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
        if key == 'min_price':
            value = 'Precio minimo: ' + utils.prettyPrice(pk_value)
        if key == 'max_price':
            value = 'Precio maximo: ' + utils.prettyPrice(pk_value)
        return value
        
    # Method that, given a key (e.g.: notebook_brand, processor, etc) and a
    # particular value for that key (usually a foreign key int), generates
    # a sensible message to alert of the current use of that filter
    def generateTitleTag(self, key, pk_value):
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
            value = 'Notebooks con ' + unicode(NotebookRamQuantity.objects.get(pk = pk_value)) + ' de RAM'
        if key == 'ram_type':
            value = 'Notebooks con memoria RAM ' + unicode(NotebookRamType.objects.get(pk = pk_value))
        if key == 'storage_type':
            value = 'Notebooks con almacenamiento de tipo ' + unicode(NotebookStorageDriveType.objects.get(pk = pk_value))
        if key == 'storage_capacity':
            value = 'Notebooks con ' + unicode(NotebookStorageDriveCapacity.objects.get(pk = pk_value)) + ' de almacenamiento'
        if key == 'screen_size_family':
            value = 'Notebooks con pantallas de ' + NotebookScreenSizeFamily.objects.get(pk = pk_value).titleText()
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
        if key == 'min_price':
            value = 'Notebooks con un precio mínimo de ' + utils.prettyPrice(pk_value)
        if key == 'max_price':
            value = 'Notebooks con un precio máximo de ' + utils.prettyPrice(pk_value)
        return value        
        
    def is_valid(self):
        return True 
        
    def save(self):
        query = '&'.join([field + '=' + str(self.__dict__[field]) for field in self.fields if self.__dict__[field]])
        search_registry = SearchRegistry()
        search_registry.query = query
        search_registry.date = date.today()
        search_registry.save()
