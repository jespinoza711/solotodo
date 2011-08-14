from django.db import models
from django.db.models import Q
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
    
    # Interface methods
    
    def get_display_name(self):
        return unicode(self.brand) + ' ' + self.gpu.name + ' (' + self.name + ')'
        
    def raw_text(self):
        result = super(VideoCard, self).base_raw_text()
        return result
        
    def load_similar_products(self):
        threshold = 4
        video_cards = VideoCard.get_valid().filter(gpu = self.gpu).filter(~Q(id = self.id)).order_by('?')[:threshold]
        self.similar_products = ','.join([str(video_card.id) for video_card in video_cards])
        
    @classmethod
    def custom_update(self):
        VideoCardGpu.update_all_tdmark_scores()
        
    @staticmethod
    def get_valid():
        return VideoCard.objects.filter(shp__isnull = False)
        
    # custom methods
    
    def pretty_memory(self):
        return unicode(self.memory_quantity) + ' ' + unicode(self.memory_type) + ' (' + unicode(self.memory_bus_width) + ')'
        
    def pretty_frequencies(self):
        return self.pretty_frequency(self.core_clock) + ' core / ' + self.pretty_frequency(self.shader_clock) + ' shaders / ' + self.pretty_frequency(self.memory_clock) + ' memorias'
        
    @staticmethod
    def pretty_frequency(value):
        return str(value) + ' MHz'
        
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card'
        ordering = ['brand', 'gpu__name', 'name']
