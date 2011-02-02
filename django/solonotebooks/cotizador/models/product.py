import operator
from datetime import date, timedelta
from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks.cotizador.models import *
from utils import prettyPrice

class Product(models.Model):
    name = models.CharField(max_length = 255)
    date_added = models.DateField()
    is_available = models.BooleanField()
    
    publicized_offer = models.ForeignKey('StoreHasProductEntity', null = True, blank = True, related_name = 'ntbk')
    min_price = models.IntegerField()
    week_visitor_count = models.IntegerField()
    week_discount = models.IntegerField()    
    
    other = models.TextField()
    long_description = models.TextField()

    similar_notebooks = models.CommaSeparatedIntegerField(max_length = 30)
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (88, 88), },
        extra_thumbnails = {
            'large': {'size': (300, 300)},
            'gallery_thumb': {'size': (90, 90)},
        },                                          
        upload_to = 'notebook_pics',
        generate_on_save = True,)

        
    def rawText(self):
        result = ''
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
        result += ' ' + self.line.rawText()
        result += ' ' + self.name
        result += ' ' + self.processor.rawText()
        result += ' ' + self.lan.rawText()
        result += ' ' + self.screen.rawText()
        result += ' ' + self.operating_system.rawText()
        result += ' ' + self.ram_type.rawText()
        result += ' ' + self.ram_frequency.rawText()
        result += ' ' + self.ram_quantity.rawText()
        result += ' ' + self.chipset.rawText()
        for video_card in self.video_card.all():
            result += ' ' + video_card.rawText()
        for video_port in self.video_port.all():
            result += ' ' + video_port.rawText()
        for storage_drive in self.storage_drive.all():
            result += ' ' + storage_drive.rawText()            
        return result
        
    def __unicode__(self):
        return self.name
        
    def pretty_min_price(self):
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
        ntbks = Notebook.objects.filter(is_available = True).filter(~Q(id = self.id))
        
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
        
    def normalize(self):
        new_price = self.storehasproduct_set.all().filter(is_available = True).filter(is_hidden = False).aggregate(Min('latest_price'))['latest_price__min']
        
        if new_price:
            print 'El notebook tiene registros de disponibilidad'
            
            log_price_change = True
            if not self.is_available:
                LogReviveNotebook.new(notebook).send_notification_mails()
                log_price_change = False
            
            if new_price != self.min_price:
                if log_price_change:
                    LogChangeNotebookPrice.new(notebook, self.min_price, new_price).send_notification_mails()
                npc = NotebookPriceChange()
                npc.notebook = notebook
                npc.price = new_price
                npc.date = date.today()
                npc.save()
                self.min_price = new_price

            self.is_available = True
        else:
            print 'El notebook no tiene registros de disponibilidad'

            if self.is_available:
                LogLostNotebook.new(notebook).send_notification_mails()
                self.is_available = False
            
        npcs = self.notebookpricechange_set.all()
        if len(npcs) == 0:
            npc = NotebookPriceChange()
            npc.notebook = notebook
            npc.price = self.min_price
            npc.date = date.today()
            npc.save()
            
        try:     
            self.publicized_offer = self.storehasproduct_set.filter(is_publicized = True, is_available = True).order_by('latest_price')[0]
        except IndexError:
            self.publicized_offer = None
            
        self.long_description = self.rawText()
        self.save()
        
        
        #similar_notebooks = [str(ntbk.id) for ntbk in self.findSimilarNotebooks()]
        #self.similar_notebooks = ','.join(similar_notebooks)
        
    def create_miniature(self):
        return { 
            'name': str(self),
            'min_price': self.min_price,
            'url': '/notebooks/' + str(self.id)
        }
        
    def price_at(self, date):
        from solonotebooks.cotizador.models import NotebookPriceChange
    
        npc = NotebookPriceChange.objects.filter(notebook = self).filter(date__lte = date).order_by('-date')
        if npc:
            return npc[0].price
        else:
            return self.min_price
            
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
        
    def print_scores(self):
        types = NotebookType.objects.all()
        for ntype in types:
            print ntype.name + ' ' + str(ntype.evaluate(self))

    @staticmethod
    def get_valid():
        return Notebook.objects.filter(is_available = True)
        
    def update_week_discount(self):
        t = date.today()
        d = timedelta(days = 7)
        old_price = self.price_at(t - d)
        try:
            self.week_discount = int(100 * (old_price - self.min_price) / old_price)
        except:
            self.week_discount = 0;
            
    def update_week_visits(self):
        t = date.today()
        d = timedelta(days = 7)
        self.week_visitor_count = len(self.notebookvisit_set.filter(date__gte = t - d))
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product'
        ordering = ['name']       
        
