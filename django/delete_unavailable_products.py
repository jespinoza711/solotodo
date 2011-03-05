import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    store = Store.objects.get(name = sys.argv[1])    
    shpes = StoreHasProductEntity.objects.filter(store = store, is_available = False)
    shpes.delete()
        
if __name__ == '__main__':
    print datetime.now()
    main()
    
