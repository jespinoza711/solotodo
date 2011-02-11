from django.db import models

class NotebookType(models.Model):
    name = models.CharField(max_length = 255)
    css_name = models.CharField(max_length = 255)
    
    ordering = models.IntegerField()
    
    screen_size = models.IntegerField()
    processor_speed = models.IntegerField()
    processor_consumption = models.IntegerField()
    video_card_speed = models.IntegerField()
    storage_quantity = models.IntegerField()
    ram_quantity = models.IntegerField()
    
    def evaluate(self, ntbk):
        from . import Notebook
        from math import fabs
        total_score = 0
        total_score += fabs(self.screen_size - ntbk.screen.size.size) * 2.0
        total_score += fabs(self.processor_speed - ntbk.processor.speed_score) / 100.0
        total_score += fabs(self.processor_consumption - ntbk.processor.consumption)
        total_score += fabs(self.video_card_speed - ntbk.video_card.order_by('-speed_score')[0].speed_score) / 200.0
        total_score += fabs(self.storage_quantity - ntbk.storage_drive.order_by('-capacity')[0].capacity.value) / 100.0
        total_score += fabs(self.ram_quantity - ntbk.ram_quantity.value)
        
        return total_score
    
    def __unicode__(self):
        return unicode(self.name)
        
    def raw_text(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook type'
        ordering = ['ordering']
