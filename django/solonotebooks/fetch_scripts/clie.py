#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Clie(FetchStore):
    name = 'Clie'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        availability_text = product_soup.findAll('td', { 'class': 'texto-neg-bold' })[-1].find('a').string.strip()
        if availability_text[0] == '0':
            return None
        
        product_name = product_soup.find('td', { 'class': 'tit-nar-bold' }).contents[0].split('&#8226;')[0].replace('&nbsp;&raquo; ', '').strip()
        product_price = int(product_soup.find('td', { 'background': 'images/ficha/bg_efectivo_d.gif' }).find('a').string.replace('$', '').replace('.', ''))
        
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
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.clie.cl/'
        urlBuscarProductos = '?ver=4&categoria_producto='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  
            ['561', 'Notebook'],
            ['542', 'Notebook'],
            ['580', 'Notebook'],
            ['564', 'Notebook'],
            ['581', 'Notebook'],
            ['562', 'Notebook'],
            ['579', 'Notebook'],
            ['575', 'Notebook'],
            ['612', 'Notebook'],
            ['598', 'Notebook'],
            ['596', 'Notebook'],
            ['595', 'Notebook'],
            ['178', 'Notebook'],
            ['500', 'Notebook'],
            ['158', 'Notebook'],
            ['307', 'Notebook'],
            ['308', 'Notebook'],
            ['646', 'Processor'],  # Procesadores Intel
            ['167', 'Screen'],  # LCD monitor
            ['551', 'Screen'],
            ['19', 'Screen'],
            ['536', 'Screen'],
            ['156', 'Screen'],
            ['310', 'Screen'],  # LCD TV monitor
            ['266', 'Screen'],
            ['550', 'Screen'],
            ['560', 'Screen'],
            ['632', 'Screen'], # LED monitor
            ['616', 'Screen'],
            ['614', 'Screen'],  # LED TV monitor
            ['26', 'Ram'],
            ['446', 'Ram'],
            ['438', 'StorageDrive'],
            ['434', 'StorageDrive'],
            ['738', 'StorageDrive'],
            ['642', 'StorageDrive'],
        ]
                            
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            num_page = 1
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&pagina=' + str(num_page)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                productNameCells = baseSoup.findAll("td", { "colspan" : "2" })
                
                names = []
                prices = []
                
                if len(productNameCells) == 0:
                    break;
                    
                for productNameCell in productNameCells:
                    link = productNameCell.find('a')['onclick'].split('\'')[1]
                    product_links.append([urlBase + link, ptype])
                    
                num_page += 1

        return product_links

