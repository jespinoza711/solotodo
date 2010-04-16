import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import date, datetime
from fetch_scripts import *
from solonotebooks.cotizador.models import *
from django.db.models import Min
from common_fetch_methods import *

def main():
    updateAvailabilityAndPrice()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
