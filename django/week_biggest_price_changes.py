import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from solonotebooks.cotizador.models import *
from datetime import date, timedelta
import operator

def main():
    ntbks = Notebook.objects.filter(is_available = True)
    
    notebook_price_changes = []
    last_week_day = date.today() - timedelta(days = 7)
    
    for ntbk in ntbks:
        latest_price = ntbk.min_price
        
        nearest_npc = NotebookPriceChange.objects.filter(notebook = ntbk).filter(date__lte = last_week_day).order_by('-date')
        
        if len(nearest_npc) == 0:
            continue
            
        nearest_price = nearest_npc[0].price
        
        if latest_price == nearest_price:
            continue
        
        notebook_price_changes.append([ntbk, latest_price - nearest_price, nearest_price, latest_price])
        
    notebook_price_changes = sorted(notebook_price_changes, key = operator.itemgetter(1))
    
    for npc in notebook_price_changes:
        print npc[0]
        print str(npc[2]) + ' - ' + str(npc[3]) + ' (' + str(npc[1]) + ')'

if __name__ == '__main__':
    main()
