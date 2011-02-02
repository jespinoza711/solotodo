import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from copy import deepcopy
from solonotebooks.cotizador.models import *
from datetime import date

def main():
    shns = StoreHasNotebook.objects.filter(is_available = True, is_hidden = True, store__name = sys.argv[1])
    for shn in shns:
        print shn.id
        print shn.custom_name
        print shn.url
        print ''
    

if __name__ == '__main__':
    main()
