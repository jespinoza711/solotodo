from django.db import models

class NotebookOperatingSystemLanguage(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Operating system language'
