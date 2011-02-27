from django.db import models

class ScreenSpeakers(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        if self.value:
            return '2x ' + str(self.value) + ' W'
        else:
            return 'No posee'
            
    def raw_text(self):
        result = ''
        if self.value:
            result = '2x ' + str(self.value) + ' W'
        return result
            
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
