#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class TecnoCl:
    name = 'Tecno.cl'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('strong').string.strip().encode('ascii', 'ignore')
        product_price = int(product_soup.findAll('table', { 'bgcolor': '#f1f1f1' })[2].findAll('td')[4].string.strip().replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def getNotebooks(self):
        print 'Getting Tecno.cl notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecno.cl/'
        urlBuscarProductos = 'prod/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  'productos.asp?cat=8',
                            'productos.asp?cat=259',
                            'productos.asp?cat=85'
                            ]
        
        product_links = []                    
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawProductLinks = baseSoup.findAll("a", { "class" : "txtchico" })
            
            
            productNames = []
            
            for rawProductLink in rawProductLinks:
                product_links.append(urlBase + urlBuscarProductos + rawProductLink['href'])

        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data


