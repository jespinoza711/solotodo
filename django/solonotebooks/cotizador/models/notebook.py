#-*- coding: UTF-8 -*-
import operator
from datetime import date, timedelta
from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import *
from utils import prettyPrice

class Notebook(Product):
    is_ram_dual_channel = models.BooleanField()
    has_bluetooth = models.BooleanField()
    has_esata = models.BooleanField()
    has_fingerprint_reader = models.BooleanField()
    has_firewire = models.BooleanField()

    battery_mah = models.IntegerField()
    battery_mwh = models.IntegerField()
    battery_mv = models.IntegerField()
    battery_cells = models.IntegerField()
    weight = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    thickness = models.IntegerField()
    usb_port_count = models.IntegerField()
    webcam_mp = models.DecimalField(max_digits = 3, decimal_places = 1)

    ntype = models.ForeignKey(NotebookType)
    line = models.ForeignKey(NotebookLine)
    processor = models.ForeignKey(NotebookProcessor)
    lan = models.ForeignKey(NotebookLan)
    screen = models.ForeignKey(NotebookScreen)
    operating_system = models.ForeignKey(NotebookOperatingSystem)
    ram_quantity = models.ForeignKey(NotebookRamQuantity)
    ram_type = models.ForeignKey(NotebookRamType)
    ram_frequency = models.ForeignKey(NotebookRamFrequency)
    chipset = models.ForeignKey(NotebookChipset)
    optical_drive = models.ForeignKey(NotebookOpticalDrive)
    wifi_card = models.ForeignKey(NotebookWifiCard)
    power_adapter = models.ForeignKey(NotebookPowerAdapter)
    card_reader = models.ForeignKey(NotebookCardReader)
    
    video_card = models.ManyToManyField(NotebookVideoCard)
    video_port = models.ManyToManyField(NotebookVideoPort)
    storage_drive = models.ManyToManyField(NotebookStorageDrive)
    
    # Interface methods
        
    def raw_text(self):
        result = super(Notebook, self).base_raw_text()
        if (self.is_ram_dual_channel):
            result += ' ram dual channel'
        if (self.has_bluetooth):
            result += ' bluetooth'
        if (self.has_esata):
            result += ' esata'
        if (self.has_firewire):
            result += ' firewire 1394'
        if (self.has_fingerprint_reader):
            result += ' fingerprint reader huella digital'
        result += ' bateria ' + str(self.battery_cells) + ' celdas ' 
        return result
        
    def update_display_name(self):
        self.display_name = unicode(self.line) + ' ' + self.name
        
    def load_similar_products(self):
        threshold = 4
        ntbks = Notebook.get_valid().filter(~Q(id = self.id))
        
        max_card_type = self.video_card.all().aggregate(Max('card_type'))['card_type__max']
        ntbks_gpu = ntbks.filter(video_card__card_type__id = max_card_type).distinct()
                
        ntbks_cpu = ntbks.filter(processor__line__family__id = self.processor.line.family.id)

        ntbks_lcd = ntbks.filter(screen__size__family__id = self.screen.size.family.id)
        
        ntbks_brand = ntbks.filter(line__brand__id = self.line.brand.id)        
                
        result_notebooks = [[ntbk, 0] for ntbk in ntbks]
        
        for result_notebook in result_notebooks:
            if result_notebook[0] in ntbks_gpu:
                # result_notebook[1] += max_card_type * max_card_type
                pass
            if result_notebook[0] in ntbks_cpu:
                result_notebook[1] += 1
            if result_notebook[0] in ntbks_lcd:
                result_notebook[1] += 1
            if result_notebook[0] in ntbks_brand:
                result_notebook[1] += 1
            if result_notebook[0].screen.is_touchscreen and self.screen.is_touchscreen:
                result_notebook[1] += 5
            result_notebook[1] -= abs(self.latest_price() - result_notebook[0].latest_price()) / 100000
            result_notebook[1] = -result_notebook[1]
        
        sorted_result_notebooks = sorted(result_notebooks, key = operator.itemgetter(1))
        if len(sorted_result_notebooks) > threshold:
            sorted_result_notebooks = sorted_result_notebooks[0:threshold]
        
        ntbks = [str(result_notebook[0].id) for result_notebook in sorted_result_notebooks]
        self.similar_products = ','.join(ntbks)
        
    @staticmethod
    def get_valid():
        return Notebook.objects.filter(shp__isnull = False)
        
    # Custom methods
        
    def prettyBattery(self):
        if (self.battery_cells == 0 and self.battery_mwh == 0 and self.battery_mv == 0 and self.battery_mah == 0):
            return ''
        if (self.battery_cells > 0):
            resultString = unicode(self.battery_cells) + ' celdas'
            if (self.battery_mwh > 0 or self.battery_mv > 0 or self.battery_mah > 0):
                resultString += ' ('
                additions = []
                if (self.battery_mah > 0):
                    additions.append(unicode(self.battery_mah) + ' mAh')
                if (self.battery_mv > 0):
                    additions.append(unicode(self.battery_mv) + ' mV')
                if (self.battery_mwh > 0):
                    additions.append(unicode(self.battery_mwh) + ' mWh')
                resultString += ' | '.join(additions) + ')'
            return resultString
        else:
            additions = []
            if (self.battery_mah > 0):
                additions.append(unicode(self.battery_mah) + ' mAh')
            if (self.battery_mv > 0):
                additions.append(unicode(self.battery_mv) + ' mV')
            if (self.battery_mwh > 0):
                additions.append(unicode(self.battery_mwh) + ' mWh')
            resultString = ' | '.join(additions)
            return resultString
            
    def prettyDimensions(self):
        if self.width == 0:
            return ''
        else:
            return unicode(self.width) + ' x ' +  unicode(self.height) + ' x ' + unicode(self.thickness) + ' mm.'
            
    def prettyVideoPorts(self):
        if len(self.video_port.all()) == 0:
            return 'No posee salidas'
        else:
            videoPorts = []
            for video_port in self.video_port.all():
                videoPorts.append(unicode(video_port))
            return ' | '.join(videoPorts)
            
    def determine_type(self):
        types = NotebookType.objects.all()
        base_score = 1000
        current_type = None
        for ntype in types:
            score = ntype.evaluate(self)
            if score < base_score:
                current_type = ntype
                base_score = score
                
        self.ntype = current_type
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook'
        ordering = ['display_name']       
        
