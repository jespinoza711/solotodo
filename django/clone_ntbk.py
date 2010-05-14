import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from copy import deepcopy
from solonotebooks.cotizador.models import *

def main():
    id_ntbk = sys.argv[1]
    ntbk = Notebook.objects.get(pk = id_ntbk)
    clone_ntbk = deepcopy(ntbk)
    clone_ntbk.id = None
    clone_ntbk.name += ' (clone)'
    clone_ntbk.save()
    print clone_ntbk.id

if __name__ == '__main__':
    main()
