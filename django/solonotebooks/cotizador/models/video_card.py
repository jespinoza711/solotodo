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
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.gpu.name + ' (' + self.name + ')'
        
    def pretty_display(self):
        return unicode(self)
        
    def raw_text(self):
        result = 'Tarjeta de video VGA GPU'
        result += ' ' + self.name
        result += ' ' + self.gpu.raw_text()
        result += ' ' + self.memory_bus_width.raw_text()
        result += ' ' + self.memory_quantity.raw_text()
        result += ' ' + self.memory_type.raw_text()
        result += ' ' + self.brand.raw_text()
        result += ' ' + self.bus.raw_text()
        result += ' ' + self.profile.raw_text()
        result += ' ' + self.slot_type.raw_text()
        result += ' ' + self.refrigeration.raw_text()
        
        for port in self.video_ports.all():
            result += ' ' + port.raw_text()
            
        return result
        
    def load_similar_products(self):
        threshold = 4
        video_cards = VideoCard.get_valid().filter(gpu = self.gpu).filter(~Q(id = self.id))[:threshold]
        self.similar_products = ','.join([str(video_card.id) for video_card in video_cards])
        
    @staticmethod
    def get_valid():
        return VideoCard.objects.filter(is_available = True)
    
    def clone_product(self):
        clone_prod = super(VideoCard, self).clone_product()

        for video_port in self.video_ports.all():
            clone_prod.video_ports.add(video_port)

        clone_prod.save()
        return clone_prod
        
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
        ordering = ['brand', 'name']
