import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

# Basic description for keeping track of each model at each store over time
class ProductData:
    def __str__(self):
        return self.custom_name + '\n' + str(self.price) + '\n' + self.url + '\n' + self.comparison_field + '\n'
        
    def __unicode__(self):
        return str(self)
        
    @staticmethod
    def retrieve_products_data(fetch_store, product_links, use_existing_links = False):
        if use_existing_links:
            store = Store.objects.get(classname = fetch_store.__class__.__name__)
            existing_shpes = store.storehasproductentity_set.all()
            existing_links = [shpe.url for shpe in existing_shpes]
            
            product_links.extend(existing_links)
            product_links = list(set(product_links))
        
        products_data = []
        num_links = len(product_links)
        
        invalid_links = []
        for idx, product_link in enumerate(product_links):
            print str(idx + 1) + ' de ' + str(num_links)
            print product_link
            product = fetch_store.retrieve_product_data(product_link)
            if product:
                print product
                products_data.append(product)
            else:
                print 'No disponible'
                invalid_links.append(product_link)
            
        print 'Links invalidos: ' + str(len(invalid_links))
        print '==================='
        for link in invalid_links:
            print link
            
        print 'Links validos: ' + str(len(products_data))
        print '=================='
        for product in products_data:
            print product.url
        for product in products_data:
            print product.price
                
        return products_data
