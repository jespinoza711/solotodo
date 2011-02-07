#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class MacOnline:
    name = 'MacOnline'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('td', { 'class': 'tit_categoria_despliegue' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('em').string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def getNotebooks(self):
        print 'Getting MacOnline notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.maconline.cl'
        urlBuscarProductos = '/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        product_links = []
        
        url_extensions = [  '178-MacBook.html',
                            '379-MacBook%20Pro.html',
                            '384-New_MacBook_Air.html'
                            ]
                            
        for url_extension in url_extensions:
            page_number = 0
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '?pagina=' + str(page_number)
                
                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                titles = baseSoup.findAll('td', { 'class' : 'nombre_producto' })
                
                if not titles:
                    break

                for i in range(len(titles)):
                    link = urlBase + titles[i].find('a')['href']
                    if link in product_links:
                        continue
                    
                    product_links.append(link)
                    
                page_number += 1
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

