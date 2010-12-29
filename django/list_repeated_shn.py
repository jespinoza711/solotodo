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
    
ntbks = Notebook.objects.all()
for ntbk in ntbks:
    shns = StoreHasNotebook.objects.filter(notebook = ntbk).filter(is_available = True).filter(is_hidden = False)
    shn_stores = set()
    for shn in shns:
        if not shn.store in stores:
            continue
            
        if shn.store in shn_stores:
            print str(ntbk.id) + ' ' + str(ntbk)
            break
        shn_stores.add(shn.store)
