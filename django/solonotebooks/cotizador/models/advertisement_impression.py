from django.db import models
from . import Advertisement

class AdvertisementImpression(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    date = models.DateField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.advertisement, self.date)
    
    class Meta:
        ordering = ['-date']
        app_label = 'cotizador'
