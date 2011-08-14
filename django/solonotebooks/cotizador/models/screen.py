#-*- coding: UTF-8 -*-
from django.db import models
from . import Product, ScreenLine, ScreenDisplay, ScreenType, ScreenSize, ScreenResolution, ScreenHasVideoPort, ScreenPanelType, ScreenSpeakers, ScreenResponseTime, ScreenRefreshRate, ScreenDigitalTuner

class Screen(Product):
    brightness = models.IntegerField()
    contrast = models.IntegerField()
    consumption = models.IntegerField()
    usb_ports = models.IntegerField()
    
    has_analog_tuner = models.BooleanField()
    is_3d = models.BooleanField()

    digital_tuner = models.ForeignKey(ScreenDigitalTuner)
    response_time = models.ForeignKey(ScreenResponseTime)
    refresh_rate = models.ForeignKey(ScreenRefreshRate)
    stype = models.ForeignKey(ScreenType)
    line = models.ForeignKey(ScreenLine)
    display = models.ForeignKey(ScreenDisplay)
    size = models.ForeignKey(ScreenSize)
    resolution  = models.ForeignKey(ScreenResolution)
    panel_type = models.ForeignKey(ScreenPanelType)
    speakers = models.ForeignKey(ScreenSpeakers)
    video_ports = models.ManyToManyField(ScreenHasVideoPort)
    
    # Interface methods

    def get_display_name(self):
        return unicode(self.line) + ' ' + self.name
        
    def raw_text(self):
        result = super(Screen, self).base_raw_text()
        if self.usb_ports:
            result += ' USB'
        if self.has_analog_tuner:
            result += u' sintonizador analogo análogo'
        return result
        
    def load_similar_products(self):
        similar_products = Screen.objects.filter(size__family = self.size.family).order_by('?')[:4]
        self.similar_products = ','.join([str(prod.id) for prod in similar_products])
        
    # Custom methods
    
    def pretty_display(self):
        return unicode(self)
    
    def pretty_contrast(self):
        if self.contrast:
            return str(self.contrast) + ':1'
        else:
            return 'Desconocido'
        
    def pretty_brightness(self):
        if self.brightness:
            return str(self.brightness) + ' cd/m<sup>2</sup>'
        else:
            return 'Desconocido'
        
    def pretty_consumption(self):
        if self.consumption:
            return str(self.consumption) + ' W'
        else:
            return 'Desconocido'
        
    def pretty_usb_ports(self):
        if self.usb_ports:
            return str(self.usb_ports)
        else:
            return 'No posee'
            
    class Meta:
        ordering = ['display_name']
        app_label = 'cotizador'
