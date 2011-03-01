import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *

# Script to test the fetch script for a store
def main():
    p = eval(sys.argv[1] + '()')
    get_store_products(p)
    
    update_availability_and_price()    
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
