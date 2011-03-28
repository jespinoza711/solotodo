import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    shpe = StoreHasProductEntity.objects.get(id = sys.argv[1])
    print shpe.dprint()
                    
if __name__ == '__main__':
    print datetime.now()
    main()
    
