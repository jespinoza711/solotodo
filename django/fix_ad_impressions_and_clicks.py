import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import date
from solonotebooks.cotizador.models import *
from random import randint

gen = []

for sv in SponsoredVisit.objects.filter(date__gte=date(2012, 9, 10)):
    gen.append(sv.date)

l = len(gen)

for idx, adv in enumerate(AdvertisementVisit.objects.filter(advertisement__store__name='HP Online')):
    print idx

    d = gen[randint(0, l - 1)]

    adv.date = d
    adv.save()

for ad in Advertisement.objects.filter(store__name='HP Online'):
    print ad

    for i in range(ad.impressions):
        print i

        idx = randint(0, l - 1)
        d = gen[idx]

        adi = AdvertisementImpression.objects.create(advertisement=ad)
        adi.date = d
        adi.save()
