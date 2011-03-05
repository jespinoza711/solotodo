import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    if len(sys.argv) > 1:
        stores = [Store.objects.get(name = sys.argv[1])]
    else:
        stores = Store.objects.all()
        
    unaccounted_links = []
        
    for store in stores:
        fs = eval(store.classname + '()')

        shpes = StoreHasProductEntity.objects.filter(store = store, is_available = False)
        for idx, shpe in enumerate(shpes):
            print str(idx) + ' de ' + str(shpes.count()) + ': ' + shpe.url
            product = shpe.retrieve_product()
            if product:
                print shpe.dprint()
                unaccounted_links.append(shpe.url)
            
    print '======================'
        
    if unaccounted_links:
        print 'Hay links sin seguimiento'
        for link in unaccounted_links:
            print link
    else:
        print 'Todos los links justificados'
        
if __name__ == '__main__':
    print datetime.now()
    main()
    
