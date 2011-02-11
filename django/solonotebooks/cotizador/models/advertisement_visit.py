from django.db import models
from . import Advertisement

class AdvertisementVisit(models.Model):
    referer_url = models.CharField(max_length = 255)
    advertisement = models.ForeignKey(Advertisement)
    
    class Meta:
        app_label = 'cotizador'
