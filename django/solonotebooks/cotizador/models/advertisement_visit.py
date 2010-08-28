from django.db import models
from solonotebooks.cotizador.models import Advertisement

class AdvertisementVisit(models.Model):
    referer_url = models.CharField(max_length = 255)
    advertisement = models.ForeignKey(Advertisement)
    
    def __unicode__(self):
        return self.embedding_html
    
    class Meta:
        app_label = 'cotizador'
