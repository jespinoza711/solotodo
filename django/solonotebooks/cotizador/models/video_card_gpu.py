from django.db import models
from solonotebooks.cotizador.models import VideoCardGpuManufacturingProcess, VideoCardGpuCore, VideoCardGpuLine, VideoCardGpuDirectxVersion, VideoCardGpuOpenglVersion, VideoCardGpuPowerConnector, VideoCardGpuCoreCount

class VideoCardGpu(models.Model):
    name = models.CharField(max_length = 255)
    
    stream_processors = models.IntegerField()
    texture_units = models.IntegerField()
    default_core_clock = models.IntegerField()
    default_shader_clock = models.IntegerField()
    default_memory_clock = models.IntegerField()
    transistor_count = models.IntegerField()
    rops = models.IntegerField()
    tdp = models.IntegerField()
    
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
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU'
        ordering = ['line__family', 'name']
