import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *

def main():
    p = eval(sys.argv[1] + '()')
    get_store_products(p, update_shpes_on_finish = True)
                
if __name__ == '__main__':
    print datetime.now()
    main()
