from django.db import models
from . import Advertisement

class AdvertisementVisit(models.Model):
    referer_url = models.CharField(max_length = 255)
    advertisement = models.ForeignKey(Advertisement)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        app_label = 'cotizador'
