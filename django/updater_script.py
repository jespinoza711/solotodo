import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks import fetch_scripts
from common_fetch_methods import *
import inspect

'''Main and all-powerful updater script, probably the backbone of the whole
site, it grabs every single model of the stores with fetchers and inserts
them into the database, logging price changes, new models and disappearing
models'''
def main():
    blacklist = ['FetchStore', 'ProductData', 'TecnoGroup', 'Cintegral']

    classnames = [classname for classname in dir(fetch_scripts) if inspect.isclass(getattr(fetch_scripts, classname)) and classname not in blacklist]
    
    stores = [eval('fetch_scripts.' + c + '()') for c in classnames]
    
    for store in stores:
        get_store_products(store)
                
    update_availability_and_price()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
