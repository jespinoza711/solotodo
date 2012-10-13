import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.advertisement_visit import AdvertisementVisit

result = []

for av in AdvertisementVisit.objects.all():
    result.append(
        (av.advertisement.target_url, str(av.date))
    )

print simplejson.dumps(result, indent=4)
