import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    products = Product.objects.all()
    for product in products:
        shps = product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price')
        if shps:
            shp = shps[0]
            if not product.is_available:
                print str(shp.id) + ' ' + str(shp)
        else:
            shp = None
            if product.is_available:
                print str(product.id) + ' ' + str(product)
                
        product.shp = shp
        product.save()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
