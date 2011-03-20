#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Impulso(FetchStore):
    name = 'Impulso'
    use_existing_links = False

    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except mechanize.HTTPError:
            return None
        product_soup = BeautifulSoup(product_data)
        
        product_title = product_soup.find('h2').string
        product_price = int(product_soup.find('span', { 'id': 'our_price_display'}).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_title
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://impulso.cl'
        urlBuscarProductos = '/prestashop/'
        
        # Browser initialization
        browser = mechanize.Browser()

        product_links = []
        
        url_extensions = [  
                            ['32-notebooks', 'Notebook'],
                            ['35-netbooks', 'Notebook'],
                            ['37-tablets', 'Notebook'],
                            ]
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            prod_list = baseSoup.find('ul', {'id': 'product_list'})
            
            if not prod_list:
                continue
            
            prod_cells = prod_list.findAll('li')

            for cell in prod_cells:
                product_links.append([cell.find('a')['href'], ptype])
                
        return product_links

