import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from common_fetch_methods import *

def main():
    ps = [Store.objects.get(classname=arg) for arg in sys.argv[1:]]
    for p in ps:
        p.update_products_from_webpage(update_shpes_on_finish = True)
                
if __name__ == '__main__':
    print datetime.now()
    main()
