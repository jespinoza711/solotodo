import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import date, datetime
from fetch_scripts import *
from solonotebooks.cotizador.models import *
from django.db.models import Min
from common_fetch_methods import *

'''Utility script to be run after inserting new products in the DB to ensure
the correct update of its minimum prices and, in general, to keep the DB sane'''

def main():
    update_availability_and_price()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
