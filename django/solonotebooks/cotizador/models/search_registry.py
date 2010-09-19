from django.db import models

class SearchRegistry(models.Model):
    query = models.TextField()
    date = models.DateField()
    
    def __unicode__(self):
        return str(self.date)
            
    class Meta:
        app_label = 'cotizador'
