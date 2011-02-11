import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from solonotebooks.cotizador.models import *
from datetime import date, timedelta
import operator

def main():
    prods = Product.objects.filter(is_available = True)
    
    product_price_changes = []
    last_week_day = date.today() - timedelta(days = 7)
    
    for prod in prods:
        latest_price = prod.min_price
        
        nearest_ppc = ProductPriceChange.objects.filter(notebook = prod).filter(date__lte = last_week_day).order_by('-date')
        
        if len(nearest_ppc) == 0:
            continue
            
        nearest_price = nearest_ppc[0].price
        
        if latest_price == nearest_price:
            continue
        
        product_price_changes.append([prod, latest_price - nearest_price, nearest_price, latest_price])
        
    product_price_changes = sorted(product_price_changes, key = operator.itemgetter(1))
    
    for ppc in product_price_changes:
        print ppc[0]
        print str(ppc[2]) + ' - ' + str(ppc[3]) + ' (' + str(ppc[1]) + ')'

if __name__ == '__main__':
    main()
