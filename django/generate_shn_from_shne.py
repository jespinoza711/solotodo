import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

shnes = StoreHasNotebookEntity.objects.filter(notebook__isnull = False)

for shne in shnes:
    print shne
    shns = StoreHasNotebook.objects.filter(store = shne.store, notebook = shne.notebook)
    if shns:
        shn = shns[0]
    else:
        shn = StoreHasNotebook()
        shne.shne = None
        shn.store = shne.store
        shn.notebook = shne.notebook
        shn.save()
        
    shne.shn = shn
    shne.save()
