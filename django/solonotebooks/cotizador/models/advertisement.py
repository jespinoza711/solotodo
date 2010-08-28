from django.db import models
from solonotebooks.cotizador.models import AdvertisementPosition

class Advertisement(models.Model):
    embedding_html = models.TextField()
    position = models.ForeignKey(AdvertisementPosition)
    target_url = models.TextField()
    impressions = models.IntegerField()
    
    class Meta:
        app_label = 'cotizador'
