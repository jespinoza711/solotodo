#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class GlobalMac(FetchStore):
    name = 'GlobalMac'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'id': 'ficha' }).find('h1').string.encode('ascii', 'ignore')
        try:
            product_price = int(product_soup.find('div', { 'class': 'price' }).find('h4').string.split('$')[1].split('pesos')[0].replace('.', ''))
        except:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.globalmac.cl/'
        urlBuscarProductos = 'ver='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['Apple/MacBook', 'Notebook'],
                            ['Apple/MacBook%20Pro', 'Notebook'],
                            ['Hardware/Monitores%20LCD', 'Screen'],
                            ['Apple/Cinema%20Display', 'Screen'],
                            ]
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            
            titles = baseSoup.findAll('h3')

            for i in range(len(titles)):
                link = titles[i].find('a')
                
                if link == None:
                	continue
                	
            	product_links.append([urlBase + link['href'], ptype])
            	
        return product_links

