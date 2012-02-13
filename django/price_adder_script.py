import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *
from django.db import transaction

# Script to test the fetch script for a store
@transaction.commit_manually
def main():
    last_price = 0
    last_valid_shpe_id = 0
    idx = 0
    for ev in ExternalVisit.objects.raw('SELECT ev.id, ev.date, ev.shn_id, sph.price from cotizador_externalvisit as ev left join cotizador_storeproducthistory as sph on (ev.shn_id = sph.registry_id and ev.date = sph.date) order by ev.shn_id, ev.date limit 40000').iterator():
        if idx % 10000 == 0:
            print idx
            #transaction.commit()
        if ev.price:
            #ev.save()
            last_price = ev.price
            last_valid_shpe_id = ev.shn.id
        else:
            if last_valid_shpe_id == ev.shn.id:
                ev.price = last_price
                #ev.save()
        idx += 1
    #transaction.commit()
                
if __name__ == '__main__':
    main()
    
