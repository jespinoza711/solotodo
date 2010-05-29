import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

ntbks = Notebook.objects.all()
for ntbk in ntbks:
    shns = StoreHasNotebook.objects.filter(notebook = ntbk).filter(is_available = True)
    stores = set()
    for shn in shns:
        if shn.store in stores:
            print str(ntbk.id) + ' ' + str(ntbk)
            break
        stores.add(shn.store)
