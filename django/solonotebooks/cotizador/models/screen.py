from django.db import models
from . import Product, ScreenLine, ScreenDisplay, ScreenType, ScreenSize, ScreenResolution, ScreenHasVideoPort, ScreenPanelType, ScreenSpeakers, ScreenResponseTime

class Screen(Product):
    brightness = models.IntegerField()
    contrast = models.IntegerField()
    consumption = models.IntegerField()
    usb_ports = models.IntegerField()
    
    has_analog_tuner = models.BooleanField()
    has_digital_tuner = models.BooleanField()
    is_3d = models.BooleanField()

    response_time = models.ForeignKey(ScreenResponseTime)
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
        result = 'Procesador CPU'
            
        return result
        
    def load_similar_products(self):
        self.similar_products = ''
        
    @staticmethod
    def get_valid():
        return Screen.objects.filter(is_available = True)
    
    def clone_product(self):
        clone_prod = super(Screen, self).clone_product()

        clone_prod.save()
        return clone_prod
        
    # Custom methods
    
    def pretty_contrast(self):
        return str(self.contrast) + ':1'
            
    class Meta:
        ordering = ['line', 'name']
        app_label = 'cotizador'
