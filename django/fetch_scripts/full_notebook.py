#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData
import urllib

class FullNotebook:
    name = 'FullNotebook'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except:
            return None
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.findAll('h2')[1].find('a').string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'id': 'esp' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def getNotebooks(self):
        print 'Getting FullNotebook notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.fullnotebook.cl/'
        urlBuscarProductos = 'tienda/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        product_links = []
        
        url_extensions = [  
                    'notebooks',
                    ]
        
        for url_extension in url_extensions:
            # Primero necesitamos el numero de paginas
            firstUrl = urlBase + urlBuscarProductos + url_extension + '/page/1'
            baseData = browser.open(firstUrl).get_data()
            baseSoup = BeautifulSoup(baseData)
            listaPags = baseSoup.find("span", {'class': 'pages'})
            last_page = int(listaPags.contents[0][-1])
            
            for i in range(last_page):
                pageUrl = urlBase + urlBuscarProductos + url_extension + '/page/' + str(i + 1)            
                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(pageUrl).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                rawLinks = baseSoup.findAll("div", { 'class':'cliente'})
                for rawLink in rawLinks:
                    product_links.append(rawLink.find("a")['href'])
                    
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)

        return products_data

