from django.db import models
from django.db.models import Q
from . import *
import mechanize
from BeautifulSoup import BeautifulSoup

class Processor(Product):
    pcmark_id = models.CharField(max_length = 255)

    frequency = models.IntegerField()
    tdp = models.IntegerField()
    min_voltage = models.IntegerField()
    max_voltage = models.IntegerField()
    pcmark_05_score = models.IntegerField()
    pcmark_vantage_score = models.IntegerField()
    passmark_score = models.IntegerField()
    
    is_64_bit = models.BooleanField()
    has_vt = models.BooleanField()
    has_smp = models.BooleanField()
    has_unlocked_multiplier = models.BooleanField()
    
    l2_cache = models.ForeignKey(ProcessorL2Cache)
    l3_cache = models.ForeignKey(ProcessorL3Cache)
    line = models.ForeignKey(ProcessorLine)
    socket = models.ForeignKey(ProcessorSocket)
    core_count = models.ForeignKey(ProcessorCoreCount)
    core = models.ForeignKey(ProcessorCore)
    multiplier = models.ForeignKey(ProcessorMultiplier)
    fsb = models.ForeignKey(ProcessorFsb)
    graphics = models.ForeignKey(ProcessorGraphics)
    turbo_modes = models.CommaSeparatedIntegerField(max_length = 50)
    
    # Interface methods
    
    def clone_product(self, staff):
        clone_prod = super(Processor, self).clone_product(staff)
        clone_prod.pcmark_id = '0'
        clone_prod.pcmark_05_score = 0
        clone_prod.pcmark_vantage_score = 0
        clone_prod.passmark_score = 0

        clone_prod.save()
        return clone_prod
    
    def get_display_name(self):
        return unicode(self.line) + self.line.family.separator + self.name

    def short_description(self):
        result = 'Procesador ' + unicode(self)
        result += ' / %s %d MHz' % (unicode(self.core_count),  self.frequency)

        return result
        
    def raw_text(self):
        result = super(Processor, self).base_raw_text()
        result += ' ' + unicode(self)
        result += ' ' + str(self.frequency)
        if self.is_64_bit:
            result += ' 64-bit 64 bit bits'
        if self.has_vt:
            result += ' virtualization virtualizacion VT'
        if self.has_smp:
            result += ' smp simultaneous multi processing hyper threading hyperthreading hyper-threading HT'
        
        return result
        
    def load_similar_products(self):
        threshold = 4
        processors = Processor.get_available().filter(core = self.core).filter(line = self.line).filter(~Q(id = self.id)).order_by('?')[:threshold]
        self.similar_products = ','.join([str(processor.id) for processor in processors])
        
    @classmethod
    def custom_update(self):
        Processor.update_all_pcmark_scores()
        
    @staticmethod
    def get_valid():
        return Processor.objects.filter(shp__isnull = False)
        
    # Mine
    
    def get_pcmark_score(self, test_id):
        base_url = 'http://3dmark.com/search?resultTypeId=' + test_id + '&linkedDisplayAdapters=1&cpuModelId=' + self.pcmark_id + '&page='
        
        page_number = 0
        scores = []
        while True:
            url = base_url + str(page_number)
            browser = mechanize.Browser()
            data = browser.open(url).get_data()
            soup = BeautifulSoup(data)
            
            score_divs = soup.findAll('div', { 'class': 'span-2 label result-table-score' })
            if not score_divs:
                break
                
            scores.extend([int(div.string) for div in score_divs if int(div.string) > 0])
            
            page_number += 1
        
        if not scores:
            return 0
        
        return sum(scores) / len(scores)
        
    @staticmethod
    def update_all_pcmark_scores():
        processors = Processor.objects.all()
        for processor in processors:
            print processor
            if processor.pcmark_id == '0':
                print 'Sin ID'
                continue
            if processor.pcmark_05_score == 0:
                print 'Actualizando PCMark 05'
                processor.update_pcmark_05_score()
            if processor.pcmark_vantage_score == 0:
                print 'Actualizando PCMark Vantage'
                processor.update_pcmark_vantage_score()
            processor.save()
        
    def update_pcmark_05_score(self):
        self.pcmark_05_score = self.get_pcmark_score('13')
        
    def update_pcmark_vantage_score(self):
        self.pcmark_vantage_score = self.get_pcmark_score('18')
        
    def pretty_cache(self):
        result = unicode(self.l2_cache) + ' L2'
        if self.l3_cache.is_valid():
            result += ' / ' + unicode(self.l3_cache) + ' L3'
        return result
        
    def pretty_voltages(self):
        if not self.min_voltage:
            return 'Desconocido'
        else:
            return str(self.min_voltage) + ' - ' + str(self.max_voltage) + ' mV'
            
    def pretty_tdp(self):
        if not self.tdp:
            return 'Desconocido'
        else:
            return str(self.tdp) + ' W'
                    
    def pretty_frequency(self):
        return unicode(self.frequency) + ' MHz'
        
    def pretty_multiplier(self):
        result = unicode(self.multiplier) + ' ('
        if self.has_unlocked_multiplier:
            result += 'Desbloqueado'
        else:
            result += 'Bloqueado'
        result += ')'
        return result
        
    def turbo_clocks(self):
        values = self.turbo_modes
        if values == '0':
            return []
        values = [int(multiplier) for multiplier in values.split(',')]
        result = [self.frequency + value * self.core.architecture.turbo_step for value in values]
        result = [str(value) + ' MHz' for value in result]
        return result
        
    
    class Meta:
        ordering = ['display_name']
        app_label = 'cotizador'
        
    
