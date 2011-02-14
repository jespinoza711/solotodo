from django.db import models
import mechanize
from BeautifulSoup import BeautifulSoup
from solonotebooks.cotizador.models import VideoCardGpuManufacturingProcess, VideoCardGpuCore, VideoCardGpuLine, VideoCardGpuDirectxVersion, VideoCardGpuOpenglVersion, VideoCardGpuPowerConnector, VideoCardGpuCoreCount

class VideoCardGpu(models.Model):
    name = models.CharField(max_length = 255)
    tdmark_id = models.CharField(max_length = 10)
    
    stream_processors = models.IntegerField()
    texture_units = models.IntegerField()
    default_core_clock = models.IntegerField()
    default_shader_clock = models.IntegerField()
    default_memory_clock = models.IntegerField()
    transistor_count = models.IntegerField()
    rops = models.IntegerField()
    tdp = models.IntegerField()
    tdmark_06_score = models.IntegerField()
    tdmark_vantage_score = models.IntegerField()
    tdmark_11_score = models.IntegerField()
    
    has_multi_gpu_support = models.BooleanField()
    
    manufacturing_process = models.ForeignKey(VideoCardGpuManufacturingProcess)
    core = models.ForeignKey(VideoCardGpuCore)
    line = models.ForeignKey(VideoCardGpuLine)
    dx_version = models.ForeignKey(VideoCardGpuDirectxVersion)
    ogl_version = models.ForeignKey(VideoCardGpuOpenglVersion)
    power_connectors = models.ForeignKey(VideoCardGpuPowerConnector)
    core_count = models.ForeignKey(VideoCardGpuCoreCount)
    
    def __unicode__(self):
        return unicode(self.line.family) + ' ' + self.name
        
    def raw_text(self):
        result = ''
        result += ' ' + self.name
        if self.has_multi_gpu_support:
            result += ' SLI CrossFire '
        result += ' ' + self.manufacturing_process.raw_text()
        result += ' ' + self.core.raw_text()
        result += ' ' + self.line.raw_text()
        result += ' ' + self.dx_version.raw_text()
        result += ' ' + self.ogl_version.raw_text()
        result += ' ' + self.power_connectors.raw_text()
        result += ' ' + self.core_count.raw_text()
        
        return result
        
    def get_tdmark_score(self, test_id):
        base_url = 'http://3dmark.com/search?resultTypeId=' + test_id + '&linkedDisplayAdapters=1&cpuModelId=0&chipsetId=' + self.tdmark_id + '&page='
        
        page_number = 0
        scores = []
        while True:
            url = base_url + str(page_number)
            print url
            browser = mechanize.Browser()
            data = browser.open(url).get_data()
            soup = BeautifulSoup(data)
            
            score_divs = soup.findAll('div', { 'class': 'span-2 label result-table-score' })
            if not score_divs:
                break
                
            scores.extend([int(div.string.replace('P', '')) for div in score_divs])
            
            page_number += 1
        
        if not scores:
            return 0
        
        return sum(scores) / len(scores)
        
    def update_tdmark_scores(self):
        self.tdmark_06_score = self.get_tdmark_score('14')
        self.tdmark_vantage_score = self.get_tdmark_score('192')
        self.tdmark_11_score = self.get_tdmark_score('232')
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU'
        ordering = ['line__family', 'name']