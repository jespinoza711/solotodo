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
    has_headphones_ouput = models.BooleanField()
    
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
    
    def __unicode__(self):
        return str(self.manufacturer) + ' ' + str(self.name)
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['manufacturer', 'name']
