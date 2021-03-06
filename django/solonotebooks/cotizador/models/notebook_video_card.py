from django.db import models
from . import NotebookVideoCardType, NotebookVideoCardLine, NotebookVideoCardMemory

class NotebookVideoCard(models.Model):
    name = models.CharField(max_length = 255)
    gpu_frequency = models.IntegerField()
    memory_frequency = models.IntegerField()
    card_type = models.ForeignKey(NotebookVideoCardType)
    line = models.ForeignKey(NotebookVideoCardLine)
    memory = models.ForeignKey(NotebookVideoCardMemory)
    speed_score = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def raw_text(self):
        return self.line.raw_text() + ' ' + self.card_type.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Video card'
        ordering = ['line', 'name']
