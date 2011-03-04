#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Cintegral(FetchStore):
    name = 'Cintegral'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('td', { 'class': 'stylenomprod' }).string.encode('ascii', 'ignore').strip()
        product_price = int(product_soup.find('td', { 'class': 'styleprod' }).string.replace('$', '').replace('.', ''))
        
        if not product_price:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        url_base = 'http://www.cintegral.cl/index.php'
        browser = mechanize.Browser()
        product_links = []
        
        url_extensions = [  #'84',   # Netbooks
                            #'9',    # Notebooks
                            #'14',   # Tarjetas de video
                            '3',    # Procesadores
                            #'1',    # LCD
                            ]
                            
        for url_extension in url_extensions:
            page_number = 1
        
            while True:
                urlWebpage = url_base + '?op=cat&id=' + url_extension + '&pagina=' + str(page_number)

                base_data = browser.open(urlWebpage).get_data()
                base_soup = BeautifulSoup(base_data)
                links = base_soup.findAll('a', { 'class' : 'style4' })[:-4]
                
                if not links:
                    break;
                
                for i in range(len(links)):
                    link = url_base + links[i]['href']
                    product_links.append(link)
                    
                page_number += 1

        return product_links

