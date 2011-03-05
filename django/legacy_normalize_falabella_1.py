import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *
import sys

# Script to test the fetch script for a store
def main():
    shpes = StoreHasProductEntity.objects.filter(store__name = 'Falabella')
    for shpe in shpes:
        base_url, args = shpe.url.split('?')
        
        try:
            d_args = args.split('&')
            d_args = dict([elem.split('=') for elem in d_args])
        except ValueError:
            #print shpe
            #print shpe.url
            print 'Delete 1'
            shpe.delete()
            continue
        
        if 'division' in d_args:    
            del d_args['division']
        else:
            #print shpe
            #print shpe.url
            print 'Delete 2'
            shpe.delete()
            continue
            
        url = base_url + '?' + '&'.join([key + '=' + value for key, value in d_args.items()])
        
        #print url
        shpe.url = url
        shpe.comparison_field = url
        shpe.save()
                
if __name__ == '__main__':
    main()
    
