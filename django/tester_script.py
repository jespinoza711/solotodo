import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

def main():
    p = PCFactory()
    analyzeStore(p)
    
    updateAvailabilityAndPrice()    
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
