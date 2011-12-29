import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    store_name = sys.argv[1]
    store = Store.objects.get(name=store_name)

    shpes = StoreHasProductEntity.objects.filter(shp__isnull=True, store=store)
    for shpe in shpes:
        other_shpes = StoreHasProductEntity.objects.filter(shp__isnull=False, store=store, custom_name=shpe.custom_name)
        print shpe.dprint()
        if other_shpes:
            shpe.shp = other_shpes[0].shp
            shpe.save()
            shpe.update(recursive=True)
            print '----'
            print other_shpes[0].dprint()
            print '----'
        else:
            print 'No match'
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
