import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    shpes = StoreHasProductEntity.objects.filter(store__name = 'PC Ofertas')
    for shpe in shpes:
        link = shpe.url
        base_link, args = link.split('?')
        args = dict([elem.split('=') for elem in args.split('&')])
        del args['path']
        args = ['%s=%s' % (k, v) for k, v in args.items()]
        link = base_link + '?' + '&'.join(args)
        print link
        try:
            shpe = StoreHasProductEntity.objects.get(url = link)
            print 'Entidad ya corregida anteriormente'
        except StoreHasProductEntity.DoesNotExist:
            shpe.url = link
            shpe.save()
            print 'Entidad corregida'
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
