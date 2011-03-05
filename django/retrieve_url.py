import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    shpe = StoreHasProductEntity.objects.get(url = sys.argv[1])
    prod = shpe.retrieve_product()
    if prod:
        print prod
        print shpe.dprint()
        
        if shpe.shp:
            print shpe.shp.product.dprint()
    else:
        print 'No disponible'
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
