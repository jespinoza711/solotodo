import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

# Script to test the fetch script for a store
def main():
    p = Bym()
    analyzeStore(p)
    
    updateAvailabilityAndPrice()    
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
