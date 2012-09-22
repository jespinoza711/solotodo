import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *
from django.db.models import Count

ais = AdvertisementImpression.objects.values('advertisement', 'date').annotate(data=Count('id')).order_by('advertisement', 'date')

ads = dict([(ad.id, ad) for ad in Advertisement.objects.all()])

for ai in ais:
    try:
        aipd = AdvertisementImpressionPerDay.objects.get(
            advertisement=ads[ai['advertisement']],
            date=ai['date'],
        )
    except AdvertisementImpressionPerDay.DoesNotExist:
        aipd = AdvertisementImpressionPerDay(
            advertisement=ads[ai['advertisement']],
            date=ai['date']
        )
        aipd.count = 0
    aipd.count += ai['data']
    aipd.save()
