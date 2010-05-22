import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import date, datetime
from fetch_scripts import *
from solonotebooks.cotizador.models import *
from django.db.models import Min
from common_fetch_methods import *

'''Utility script to be run after inserting new notebooks in the DB to ensure
te correct update of its minimum prices and, in general, to keep the DB sane'''

def main():
    updateAvailabilityAndPrice()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
