#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Racle(FetchStore):
    name = 'Racle'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        try:
            product_name = product_soup.findAll('h1')[1].string.encode('ascii', 'ignore').strip()
        except Exception:
            return None
        product_price = int(product_soup.find('span', { 'class': 'precio_efectivo' }).string.split(':')[1].replace('.', '').replace('$', '').replace(' ', '').strip())
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data
    
    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.racle.cl'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        urlSearch = '/ventas/component/virtuemart/?category_id='            

        urlExtensions = [
                            ['21', 'Notebook'], 
                            ['83', 'Notebook'],
                            ['755', 'Screen'],
                        ]
        product_links = []
        for urlExtension, ptype in urlExtensions:
            urlWebpage = urlBase + urlSearch + urlExtension + '&page=shop.browse&limit=50&limitstart=0'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productDetailsRows = baseSoup.find('form', {'name': 'order'}).parent.find('table').findAll('tr', recursive=False)
            cells = []
            
            for tr in productDetailsRows:
                cells.extend(tr.findAll('td', recursive=False))
            
            
            for cell in cells:
                productLink = cell.find('a')
                if not productLink:
                    continue
                product_links.append([urlBase + productLink['href'], ptype])
            
        return product_links

