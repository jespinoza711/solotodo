import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *

try:
    store_name = sys.argv[1]
    stores = Store.objects.filter(name = store_name)
except:
    stores = Store.objects.all()
    
shps = StoreHasProduct.objects.all()

for shp in shps:
    shpes = shp.storehasproductentity_set.filter(is_available = True).filter(is_hidden = False)
    
    if len(shpes) > 1 and shp.store in stores:
        print str(shp.product.id) + ' - ' + unicode(shp)
        for shpe in shpes:
            print '* ' + str(shpe.id)
