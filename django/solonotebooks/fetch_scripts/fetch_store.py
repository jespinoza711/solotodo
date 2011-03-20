#!/usr/bin/env python

from . import ProductData
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

class FetchStore:
    def get_products(self):
        print 'Getting ' + self.name + ' products'
        product_links = self.retrieve_product_links()
        
        return self.retrieve_products_data(product_links)
        
        
    def retrieve_products_data(self, product_links):        
        products_data = []
        num_links = len(product_links)
        
        invalid_links = []
        for idx, product_link_data in enumerate(product_links):
            product_link = product_link_data[0]
            ptype = product_link_data[1]
            print str(idx + 1) + ' de ' + str(num_links)
            print product_link
            product = self.retrieve_product_data(product_link)
            if product:
                product.ptype = ptype
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
