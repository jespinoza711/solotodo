import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

try:
    store_name = sys.argv[1]
    stores = Store.objects.filter(name = store_name)
except:
    stores = Store.objects.all()
    
shns = StoreHasProduct.objects.all()

for shn in shns:
    shnes = shn.storehasproductentity_set.filter(is_available = True).filter(is_hidden = False)
    
    if len(shnes) > 1 and shn.store in stores:
        print str(shn.notebook.id) + ' - ' + unicode(shn)
        for shne in shnes:
            print '* ' + str(shne.id)
