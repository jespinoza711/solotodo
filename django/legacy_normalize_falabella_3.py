import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *
import sys

# Script to test the fetch script for a store
def main():
    shpes = StoreHasProductEntity.objects.filter(store__name = 'Falabella')
    urls = []
    
    for shpe in shpes:
        if shpe.url in urls:
            print shpe.dprint()
        else:
            urls.append(shpe.url)
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
