from django.db import models
from . import Advertisement

class AdvertisementVisit(models.Model):
    referer_url = models.CharField(max_length = 255)
    advertisement = models.ForeignKey(Advertisement)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.advertisement, self.date)
    
    class Meta:
        app_label = 'cotizador'
