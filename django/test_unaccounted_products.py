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
        
        default_products = [product.url for product in fs.get_products()]
        all_products = [product.url for product in fs.get_products(use_existing_links = True)]
        
        for link in all_products:
            if link not in default_products:
                unaccounted_links.append(link)
        
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
    
