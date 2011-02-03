from django.db import models
from . import AdvertisementPosition

class Advertisement(models.Model):
    name = models.CharField(max_length = 255)
    embedding_html = models.TextField()
    position = models.ForeignKey(AdvertisementPosition)
    target_url = models.TextField()
    impressions = models.IntegerField()
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return unicode(self.name)   
    
    class Meta:
        app_label = 'cotizador'
