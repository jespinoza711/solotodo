import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from copy import deepcopy
from solonotebooks.cotizador.models import *
from datetime import date

def main():
    pendings_shpes = StoreHasProductEntity.objects.filter(shp__isnull=True, store__name='Racle')
    for shpe in pendings_shpes:
        print shpe
        compatible_shpes = StoreHasProductEntity.objects.filter(shp__isnull=False, custom_name=shpe.custom_name, store__name='Racle')
        if compatible_shpes:
            print compatible_shpes[0]
            shpe.shp = compatible_shpes[0].shp
            shpe.save()
            shpe.update(recursive = True)
        else:
            print 'No encontrado'
    

if __name__ == '__main__':
    main()
