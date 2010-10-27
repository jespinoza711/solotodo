import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

'''Main and all-powerful updater script, probably the backbone of the whole
site, it grabs every single model of the stores with fetchers and inserts
them into the database, logging price changes, new models and disappearing
models'''
def main():
    for shn in StoreHasNotebook.objects.all():
        print shn
        shn.prevent_availability_change = False
        shn.save()

    stores = [NotebookCenter(), PackardBell(), Bip(), LaPolar(), Bym(), Clie(), Falabella(), ENotebook(), FullNotebook(), Paris(), PCFactory(), Sym(), TecnoCl(), Wei(), Sistemax(), Dell(), Webco(), Ripley(), Racle(), Magens(), GlobalMac(), Syd(), MacOnline(), RkNotebooks(), Impulso(), Peta(), HPOnline(), PortatilChile(), TecnoGroup()]
    
    for store in stores:
        getStoreNotebooks(store)
                
    updateAvailabilityAndPrice()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
