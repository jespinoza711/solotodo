#!/usr/bin/env python

from . import ProductData
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

class FetchStore:
    def get_products(self, use_existing_links = None):
        print 'Getting ' + self.name + ' products'
        product_links = self.retrieve_product_links()
        
        if use_existing_links is None:
            use_existing_links = self.use_existing_links
        return self.retrieve_products_data(product_links, use_existing_links = use_existing_links)
        
        
    def retrieve_products_data(self, product_links, use_existing_links = False):
        if use_existing_links:
            store = Store.objects.get(classname = self.__class__.__name__)
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
            product = self.retrieve_product_data(product_link)
            if product:
                print product
                products_data.append(product)
            else:
                print 'No disponible'
                invalid_links.append(product_link)
            
        print 'Links no disponibles: ' + str(len(invalid_links))
        print '========================='
        for link in invalid_links:
            print link
                
        return products_data
