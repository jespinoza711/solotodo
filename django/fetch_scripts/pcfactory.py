#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCFactory:
    name = 'PCFactory'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        baseData = browser.open(product_link).get_data()
        baseSoup = BeautifulSoup(baseData)
        product_data = ProductData()
        
        available_cells = baseSoup.findAll('table', { 'class' : 'ProductLine1' })[2].findAll('td')
        if len(available_cells) != 1:
            availability_string = available_cells[2].string
            if availability_string == 'Agotado':      
                return None
        
        titleSpan = baseSoup.find('span', { 'class' : 'productoFicha' })
        product_data.custom_name = titleSpan.find('strong').string.encode('ascii', 'ignore')
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        priceSpan = baseSoup.find('span', { 'id' : 'simulador' })
        product_data.price = int(priceSpan.string.replace('.', ''))
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting PCFactory notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcfactory.cl'
        urlBuscarProductos = '/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  
                            '?papa=24&categoria=424',
                            '?papa=24&categoria=449',
                            '?papa=24&categoria=410',
                            '?papa=24&categoria=437',
                            '?papa=24&categoria=436',
                            ]
                          
        pageLinks = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            pageNumber = 1
            
            localLinks = []
                
            while True:
                completeWebpage = urlWebpage + '&pagina=' + str(pageNumber)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkLinks = baseSoup.findAll('a', { 'class' : 'vinculoNombreProd' })
                trigger = False
                for ntbkLink in ntbkLinks:
                    link = urlBase + ntbkLink['href']
                    link = link.encode('ascii', 'ignore')
                    if link in localLinks:
                        trigger = True
                        break
                    localLinks.append(link)
                    
                if trigger:
                    pageLinks.extend(localLinks)
                    break
                    
                pageNumber += 1
                
        pageLinks = list(set(pageLinks))

        for link in pageLinks:
            product = self.retrieve_product_data(link)
            if product:
                productsData.append(product)

        return productsData

