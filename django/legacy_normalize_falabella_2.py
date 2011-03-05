import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *
import sys

# Script to test the fetch script for a store
def main():
    top_shpes = StoreHasProductEntity.objects.filter(store__name = 'Falabella')
    urls = list(set([shpe.url for shpe in top_shpes]))
    
    for url in urls:
        shpes = StoreHasProductEntity.objects.filter(url = url).order_by('-id')
        main_shpe = shpes[0]
        sub_shpes = shpes[1:]
        if shpes:
            print main_shpe.dprint()
            for shpe in sub_shpes:
                print shpe.dprint()
                shpe.delete()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
