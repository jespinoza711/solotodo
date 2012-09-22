import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *
from django.db.models import Count

ais = AdvertisementImpression.objects.values('advertisement', 'date').annotate(data=Count('id')).order_by('advertisement', 'date')

ads = dict([(ad.id, ad) for ad in Advertisement.objects.all()])

for ai in ais:
    AdvertisementImpressionPerDay.objects.create(
        advertisement=ads[ai['advertisement']],
        date=ai['date'],
        count=ai['data']
    )
