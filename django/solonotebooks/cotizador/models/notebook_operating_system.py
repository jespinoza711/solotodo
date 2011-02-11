from django.db import models
from . import NotebookOperatingSystemFamily, NotebookOperatingSystemLanguage

class NotebookOperatingSystem(models.Model):
    name = models.CharField(max_length = 255)
    is_64_bit = models.BooleanField()
    family = models.ForeignKey(NotebookOperatingSystemFamily)
    language = models.ForeignKey(NotebookOperatingSystemLanguage)
    
    def __unicode__(self):
        result = unicode(self.family) + ' ' + self.name
        if self.is_64_bit:
            result += ' (64 bits)'
        return result
        
    def raw_text(self):
        result = self.family.raw_text() + ' ' + self.name
        if self.is_64_bit:
            result += ' 64 bits'
        return result
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Operating system'
        ordering = ['family', 'name']
