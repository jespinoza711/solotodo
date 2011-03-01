import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from solonotebooks.cotizador.models import *
from datetime import date

def main():
    shpes = StoreHasProductEntity.objects.all()
    for shpe in shpes:
        if shpe.shp:
            store = shpe.shp.store
        else:
            store = shpe.infer_store()
        if not store:
            print str(shpe.id) + ' ' + str(shpe)
            print shpe.url
            shpe.delete()
            
        shpe.store = store
        shpe.save()
            

if __name__ == '__main__':
    main()
