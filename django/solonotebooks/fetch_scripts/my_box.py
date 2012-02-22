#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class MyBox(FetchStore):
    name = 'MyBox'
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
        urlBase = 'http://mybox.cl'
        
        # Browser initialization
        browser = mechanize.Browser()

        product_links = []
        
        url_extensions = [  
            ['38-notebooks', 'Notebook'],
            ['7-monitores-y-proyectores', 'Screen'],
            ['41-placas-madre', 'Motherboard'],
            ['44-procesadores', 'Processor'],
            ['54-tarjetas-de-video', 'VideoCard'],
            ['28-memoria-ram', 'Ram'],
            ['5-discos-duros', 'StorageDrive'],
            ['19-fuentes-de-poder', 'PowerSupply'],
        ]
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + '/' + url_extension + '?n=50'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            prod_list = baseSoup.find('ul', {'id': 'product_list'})
            
            if not prod_list:
                continue
            
            prod_cells = prod_list.findAll('li')

            for cell in prod_cells:
                product_links.append([urlBase + cell.find('a')['href'], ptype])
                
        return product_links

