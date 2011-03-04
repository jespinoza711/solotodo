import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    s = Store.objects.get(name = sys.argv[1])
    fs = eval(s.classname + '()')
    
    shpes = s.storehasproductentity_set.all()
    len_shpes = len(shpes)

    for idx, shpe in enumerate(shpes):
        print str(idx) + ' de ' + str(len_shpes)
        print shpe.url
        p = fs.retrieve_product_data(shpe.url)
        if shpe.is_available and not p:
            print a_shpe.dprint()
            print 'Should not be None!'
        elif not shpe.is_available and p:
            print shpe.dprint()
            print 'Should be None!'

                
if __name__ == '__main__':
    print datetime.now()
    main()
    
