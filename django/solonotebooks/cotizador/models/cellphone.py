#-*- coding: UTF-8 -*-
from django.db import models
from . import *

class Cellphone(models.Model):
    name = models.CharField(max_length = 255)

    weight = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    depth = models.IntegerField()
    internal_memory = models.IntegerField()
    battery = models.IntegerField()
    
    records_video = models.BooleanField()
    plays_mp3 = models.BooleanField()
    has_bluetooth = models.BooleanField()
    has_wifi = models.BooleanField()
    has_3g = models.BooleanField()
    has_gps = models.BooleanField()
    has_headphones_output = models.BooleanField()
    
    form_factor = models.ForeignKey(CellphoneFormFactor)
    category = models.ForeignKey(CellphoneCategory)
    graphics = models.ForeignKey(CellphoneGraphics, null = True, blank = True)
    ram = models.ForeignKey(CellphoneRam)
    manufacturer = models.ForeignKey(CellphoneManufacturer)
    operating_system = models.ForeignKey(CellphoneOperatingSystem)
    keyboard = models.ForeignKey(CellphoneKeyboard)
    camera = models.ForeignKey(CellphoneCamera)
    card_reader = models.ForeignKey(CellphoneCardReader)
    screen = models.ForeignKey(CellphoneScreen)
    processor = models.ForeignKey(CellphoneProcessor, null = True, blank = True)
    
    def pretty_weight(self):
        if self.weight:
            return str(self.weight) + ' g.'
        else:
            return 'Desconocido'
            
    def pretty_internal_memory(self):
        if self.internal_memory:
            return str(self.internal_memory) + ' MB'
        else:
            return 'Desconocido'
            
    def pretty_battery(self):
        if self.battery:
            return str(self.battery) + ' mAh'
        else:
            return 'Desconocido'
            
    def pretty_dimensions(self):
        if self.width:
            return str(self.width) + ' x ' + str(self.height) + ' x ' + str(self.depth) + ' mm.'
        else:
            return 'Desconocido'
    
    def __unicode__(self):
        return str(self.manufacturer) + ' ' + str(self.name)
        
    def raw_text(self):
        result = self.name
        for field in self._meta.fields:
            if field.__class__.__name__ == 'ForeignKey':
                name = field.get_attname().replace('_id', '')
                if name == 'shp' or name == 'sponsored_shp':
                    continue
                attribute = getattr(self, name)
                if attribute:
                    result += ' ' + attribute.raw_text().encode('ascii', 'ignore')
                
        if self.records_video:
            result += u' grabación grabacion video vídeo'
        if self.plays_mp3 :
            result += ' reproductor reproduce mp3'
        if self.has_bluetooth:
            result += ' bluetooth'
        if self.has_wifi:
            result += ' wifi wi-fi wi fi'
        if self.has_3g:
            result += ' 3g hsdpa hsupa umts'
        if self.has_gps:
            result += ' gps agps a-gps'
        if self.has_headphones_output:
            result += u' audifonos audífonos 3,5 3.5 3,5mm 3.5mm'
            
        return result
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['manufacturer', 'name']
