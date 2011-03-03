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

    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def raw_text(self):
        result = 'Pantalla'
        if self.usb_ports:
            result += ' USB'
        if self.has_analog_tuner:
            result += u' sintonizador analogo análogo'
        result += ' ' + self.name
        result += ' ' + self.digital_tuner.raw_text()
        result += ' ' + self.response_time.raw_text()
        result += ' ' + self.refresh_rate.raw_text()
        result += ' ' + self.stype.raw_text()
        result += ' ' + self.line.raw_text()
        result += ' ' + self.display.raw_text()
        result += ' ' + self.size.raw_text()
        result += ' ' + self.resolution.raw_text()
        result += ' ' + self.panel_type.raw_text()
        result += ' ' + self.speakers.raw_text()
        for port in self.video_ports.all():
            result += ' ' + port.raw_text()
            
        return result
        
    def load_similar_products(self):
        similar_products = Screen.objects.filter(size__family = self.size.family).order_by('?')[:4]
        self.similar_products = ','.join([str(prod.id) for prod in similar_products])
        
    @staticmethod
    def get_valid():
        return Screen.objects.filter(shp__isnull = False)
    
    def clone_product(self):
        clone_prod = super(Screen, self).clone_product()
        
        for video_port in self.video_ports.all():
            clone_prod.video_ports.add(video_port)

        clone_prod.save()
        return clone_prod
        
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
        ordering = ['line', 'name']
        app_label = 'cotizador'
