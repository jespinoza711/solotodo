#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class TecnoCl(FetchStore):
    name = 'Tecno.cl'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('strong').string.strip().encode('ascii', 'ignore')
        product_price = int(product_soup.findAll('table', { 'bgcolor': '#f1f1f1' })[2].findAll('td')[2].string.strip().replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecno.cl/'
        urlBuscarProductos = 'prod/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['productos.asp?cat=8', 'Notebook'],
                            ['productos.asp?cat=259', 'Notebook'],
                            ['productos.asp?cat=85', 'Notebook'],
                            ['productos.asp?cat=50', 'Notebook'],
                            ['productos.asp?cat=244', 'Processor'],    # Procesadores AMD
                            ['productos.asp?cat=251', 'Processor'],    # Procesadores Intel
                            ['productos.asp?cat=217', 'Screen'],    # LCD 15
                            ['productos.asp?cat=40', 'Screen'],     # LCD 17
                            ['productos.asp?cat=218', 'Screen'],    # LCD 19+
                            ['productos.asp?cat=87', 'Screen'],    # LCDTV
                            ]
        
        product_links = []                    
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawProductLinks = baseSoup.findAll("a", { "class" : "txtchico" })
            
            
            productNames = []
            
            for rawProductLink in rawProductLinks:
                product_links.append([urlBase + urlBuscarProductos + rawProductLink['href'], ptype])

        return product_links


