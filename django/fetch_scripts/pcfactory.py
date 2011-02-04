#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCFactory:
    name = 'PCFactory'

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
        
        url_extensions = [  '?papa=24&categoria=424',
                            '?papa=24&categoria=449',
                            '?papa=24&categoria=410',
                            '?papa=24&categoria=437',
                            '?papa=24&categoria=436'
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
            baseData = browser.open(link).get_data()
            baseSoup = BeautifulSoup(baseData)
            productData = ProductData()
            titleSpan = baseSoup.find('span', { 'class' : 'productoFicha' })
            productData.custom_name = titleSpan.find('strong').string.encode('ascii', 'ignore')
            productData.url = link
            productData.comparison_field = link
            
            priceSpan = baseSoup.find('span', { 'id' : 'simulador' })
            productData.price = int(priceSpan.string.replace('.', ''))
            print productData
            productsData.append(productData)

        return productsData

