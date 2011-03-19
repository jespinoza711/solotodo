import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    fetch_store = eval(sys.argv[1] + '()')
    url = sys.argv[2]
    prod = fetch_store.retrieve_product_data(url)
    if prod:
        print prod
    else:
        print 'No disponible'
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
