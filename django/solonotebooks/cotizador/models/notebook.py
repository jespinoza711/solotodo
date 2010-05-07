import operator
from django.db import models
from django.db.models import Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks.cotizador.models import Processor, OpticalDrive, NotebookLine, Lan
from solonotebooks.cotizador.models import OperatingSystem, VideoCard, VideoPort, Screen
from solonotebooks.cotizador.models import StorageDrive, WifiCard, Chipset, RamQuantity
from solonotebooks.cotizador.models import RamType, RamFrequency, PowerAdapter
from solonotebooks.cotizador.models import NotebookCardReader
from utils import prettyPrice


class Notebook(models.Model):
    name = models.CharField(max_length = 255)
    
    is_ram_dual_channel = models.BooleanField()
    has_bluetooth = models.BooleanField()
    has_esata = models.BooleanField()
    has_fingerprint_reader = models.BooleanField()
    has_firewire = models.BooleanField()
    is_available = models.BooleanField()
    
    battery_mah = models.IntegerField()
    battery_mwh = models.IntegerField()
    battery_mv = models.IntegerField()
    battery_cells = models.IntegerField()
    weight = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    thickness = models.IntegerField()
    usb_port_count = models.IntegerField()
    min_price = models.IntegerField()
    webcam_mp = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    other = models.TextField()
    
    line = models.ForeignKey(NotebookLine)
    processor = models.ForeignKey(Processor)
    lan = models.ForeignKey(Lan)
    screen = models.ForeignKey(Screen)
    operating_system = models.ForeignKey(OperatingSystem)
    ram_quantity = models.ForeignKey(RamQuantity)
    ram_type = models.ForeignKey(RamType)
    ram_frequency = models.ForeignKey(RamFrequency)
    chipset = models.ForeignKey(Chipset)
    optical_drive = models.ForeignKey(OpticalDrive)
    wifi_card = models.ForeignKey(WifiCard)
    power_adapter = models.ForeignKey(PowerAdapter)
    card_reader = models.ForeignKey(NotebookCardReader)
    
    video_card = models.ManyToManyField(VideoCard)
    video_port = models.ManyToManyField(VideoPort)
    storage_drive = models.ManyToManyField(StorageDrive)    
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (120, 120), },
        extra_thumbnails = {
            'large': {'size': (300, 300)},
            'gallery_thumb': {'size': (90, 90)},
        },                                          
        upload_to = 'notebook_pics',
        generate_on_save = True,)
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def prettyMinPrice(self):
        return prettyPrice(self.min_price)
        
    def prettyMaxPrice(self):
        return prettyPrice(self.max_price)
        
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

            
    def findSimilarNotebooks(self):
        threshold = 4
        ntbks = Notebook.objects.filter(is_available=True).filter(~Q(id = self.id))
        
        max_card_type = self.video_card.all().aggregate(Max('card_type'))['card_type__max']
        ntbks_gpu = ntbks.filter(video_card__card_type__id = max_card_type).distinct()
                
        ntbks_cpu = ntbks.filter(processor__line__family__id = self.processor.line.family.id)

        ntbks_lcd = ntbks.filter(screen__size__family__id = self.screen.size.family.id)
        
        ntbks_brand = ntbks.filter(line__brand__id = self.line.brand.id)        
                
        result_notebooks = [[ntbk, 0] for ntbk in ntbks]
        
        for result_notebook in result_notebooks:
            if result_notebook[0] in ntbks_gpu:
                result_notebook[1] += max_card_type * max_card_type
            if result_notebook[0] in ntbks_cpu:
                result_notebook[1] += 1
            if result_notebook[0] in ntbks_lcd:
                result_notebook[1] += 1
            if result_notebook[0] in ntbks_brand:
                result_notebook[1] += 1
            if result_notebook[0].screen.is_touchscreen and self.screen.is_touchscreen:
                result_notebook[1] += 5
            result_notebook[1] -= abs(self.min_price - result_notebook[0].min_price) / 100000
            result_notebook[1] = -result_notebook[1]
        
        sorted_result_notebooks = sorted(result_notebooks, key = operator.itemgetter(1))
        if len(sorted_result_notebooks) > threshold:
            sorted_result_notebooks = sorted_result_notebooks[0:threshold]
        
        ntbks = [result_notebook[0] for result_notebook in sorted_result_notebooks]

        return ntbks
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook'
        ordering = ['line', 'name']
