import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.advertisement_impression_per_day import AdvertisementImpressionPerDay

result = []

for aipd in AdvertisementImpressionPerDay.objects.all():
    result.append(
        (aipd.advertisement.target_url, str(aipd.date), aipd.count)
    )

print simplejson.dumps(result, indent=4)
