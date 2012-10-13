import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.sponsored_visit import SponsoredVisit

result = []

for sv in SponsoredVisit.objects.all():
    if sv.shp.shpe:
        result.append(
            (sv.shp.shpe.url, str(sv.date))
        )

print simplejson.dumps(result, indent=4)
