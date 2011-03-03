import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    product = Product.objects.get(pk = 1083)
    product.update()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
