import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from copy import deepcopy
from solonotebooks.cotizador.models import *

''' Utility method for cloning a notebook (useful when indexing and finding a 
model very similar - but not equal - to one already in the database '''
def main():
    id_ntbk = sys.argv[1]
    ntbk = Notebook.objects.get(pk = id_ntbk)
    clone_ntbk = deepcopy(ntbk)
    clone_ntbk.id = None
    clone_ntbk.name += ' (clone)'
    clone_ntbk.save()

    # Since VGAs and SDs are linked in another table, clone those links too
    for video_card in ntbk.video_card.all():
        clone_ntbk.video_card.add(video_card)

    for video_port in ntbk.video_port.all():
        clone_ntbk.video_port.add(video_port)

    for storage_drive in ntbk.storage_drive.all():
        clone_ntbk.storage_drive.add(storage_drive)

    clone_ntbk.save()

    print clone_ntbk.id

if __name__ == '__main__':
    main()
