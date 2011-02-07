#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Cintegral:
    name = 'Cintegral'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('td', { 'class': 'stylenomprod' }).string.strip()
        product_price = int(product_soup.find('td', { 'class': 'styleprod' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def getNotebooks(self):
        print 'Getting Cintegral notebooks'
        # Basic data of the target webpage and the specific catalog
        url_base = 'http://www.cintegral.cl/index.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        product_links = []
        
        url_extensions = [  '84',   # Netbooks
                            '9',    # Notebooks
                            ]
                            
        for url_extension in url_extensions:
            page_number = 1
        
            while True:
                urlWebpage = url_base + '?op=cat&id=' + url_extension + '&pagina=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                base_data = browser.open(urlWebpage).get_data()
                base_soup = BeautifulSoup(base_data)
                

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                links = base_soup.findAll('a', { 'class' : 'style4' })[:-4]
                
                if not links:
                    break;
                
                for i in range(len(links)):
                    link = url_base + links[i]['href']
                    product_links.append(link)
                    
                page_number += 1
        
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            products_data.append(product)

        return products_data

