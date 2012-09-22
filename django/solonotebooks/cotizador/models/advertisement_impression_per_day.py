from django.db import models
from . import Advertisement

class AdvertisementImpressionPerDay(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    date = models.DateField(db_index=True)
    count = models.IntegerField()

    def __unicode__(self):
        return u'{0} - {1}: {2}'.format(self.advertisement, self.date, self.count)
    
    class Meta:
        unique_together = ('advertisement', 'date')
        ordering = ['-date']
        app_label = 'cotizador'
