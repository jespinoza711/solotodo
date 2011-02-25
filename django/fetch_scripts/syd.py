#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Syd:
    name = 'Syd'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.findAll('h2')[5].string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('div', { 'class': 'detallesCompra' }).findAll('dd')[1].string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting Syd notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.syd.cl'
        urlBuscarProductos = ''
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  '/computadoras/macbook_pro',
                            '/computadoras/macbook',
                            '/computadoras/macbook_air',
                            '/computadoras/monitores',
                            ]
        
        product_links = []                    
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension + '/?op=all&crit='

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            titles = baseSoup.findAll('h4')

            for i in range(len(titles)):
                link = titles[i].find('a')
                product_links.append(urlBase + urlBuscarProductos + url_extension + '/' + link['href'])
			
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

