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

    for shp in StoreHasProduct.objects.all():
        print shp
        shp.prevent_availability_change = False
        shp.save()

    stores = [NotebookCenter(), PackardBell(), LaPolar(), Bym(), Clie(), Falabella(), ENotebook(), FullNotebook(), Paris(), PCFactory(), Sym(), TecnoCl(), Wei(), Sistemax(), Dell(), Webco(), Racle(), Magens(), GlobalMac(), Syd(), MacOnline(), Impulso(), Peta(), HPOnline(), PortatilChile(), TecnoGroup(), Ripley(), AbcDin(), Cintegral(), Rigam(), PCOfertas(), Bip(), RkNotebooks()]
    
    for store in stores:
        get_store_products(store)
                
    update_availability_and_price()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
