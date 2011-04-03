from django.db import models

class CellphoneProcessor(models.Model):
    name = models.CharField(max_length = 255)
    frequency = models.IntegerField()
    
    def __unicode__(self):
        result = self.name
        if self.frequency:
            result += ' (' + str(self.frequency) + ' MHz)'
        return result
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['name']
