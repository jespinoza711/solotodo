from django.db import models
from solonotebooks.cotizador.models import Product, VideoCardGpu, VideoCardMemoryBusWidth, VideoCardMemoryQuantity, VideoCardMemoryType, VideoCardBrand, VideoCardBus, VideoCardProfile, VideoCardSlotType, VideoCardRefrigeration, VideoCardHasPort

class VideoCard(Product):
    core_clock = models.IntegerField()
    shader_clock = models.IntegerField()
    memory_clock = models.IntegerField()
    
    gpu = models.ForeignKey(VideoCardGpu)
    memory_bus_width = models.ForeignKey(VideoCardMemoryBusWidth)
    memory_quantity = models.ForeignKey(VideoCardMemoryQuantity)
    memory_type = models.ForeignKey(VideoCardMemoryType)
    brand = models.ForeignKey(VideoCardBrand)
    bus = models.ForeignKey(VideoCardBus)
    profile = models.ForeignKey(VideoCardProfile)
    slot_type = models.ForeignKey(VideoCardSlotType)
    refrigeration = models.ForeignKey(VideoCardRefrigeration)
    
    video_ports = models.ManyToManyField(VideoCardHasPort)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card'
        ordering = ['brand', 'name']
