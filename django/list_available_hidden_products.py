import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from copy import deepcopy
from solonotebooks.cotizador.models import *
from datetime import date

def main():
    shpes = StoreHasProductEntity.objects.filter(is_available = True, is_hidden = True, shp__store__name = sys.argv[1])
    for shpe in shpes:
        print shpe.id
        print shpe.custom_name
        print shpe.url
        print ''
    

if __name__ == '__main__':
    main()
