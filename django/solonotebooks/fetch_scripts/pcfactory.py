#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PCFactory(FetchStore):
    name = 'PCFactory'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        try:
            browser = mechanize.Browser()
            baseData = browser.open(product_link).get_data()
            baseSoup = BeautifulSoup(baseData)
            product_data = ProductData()
            
            available_cells = baseSoup.findAll('table', { 'class' : 'ProductLine1' })[2].findAll('td')
            if len(available_cells) != 1:
                availability_cells = available_cells[2::2]
                for cell in availability_cells:
                    if cell.string == 'Agotado':      
                        return None
            
            titleSpan = baseSoup.find('span', { 'class' : 'productoFicha' })
            product_data.custom_name = titleSpan.find('strong').string.encode('ascii', 'ignore')
            product_data.url = product_link
            product_data.comparison_field = product_link
            
            price_data = int(baseSoup.find('select', { 'class' : 'PCFdropFicha' }).findAll('option')[1]['value'].replace('.', ''))
            product_data.price = price_data
            
            return product_data
        except:
            return None

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcfactory.cl'
        urlBuscarProductos = '/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  
                            '?papa=24&categoria=424',   # Notebooks 7 a 11
                            '?papa=24&categoria=449',   # Notebooks 12 a 13
                            '?papa=24&categoria=410',   # Notebooks 14
                            '?papa=24&categoria=437',   # Notebooks 15
                            '?papa=24&categoria=436',   # Notebooks 16 y +
                            '?papa=334&categoria=40',   # VGA AGP
                            '?papa=334&categoria=378',  # VGA PCIe Nvidia
                            '?papa=334&categoria=454',  # VGA PCIe ATI
                            '?papa=334&categoria=455',  # VGA Profesionales
                            '?papa=272&categoria=409',  # CPU Server
                            '?papa=272&categoria=465',  # CPU AM3
                            '?papa=272&categoria=388',  # CPU 775
                            '?papa=272&categoria=468',  # CPU 1156
                            '?papa=272&categoria=446',  # CPU 1366
                            '?papa=256&categoria=250',  # Monitores LCD
                            '?papa=256&categoria=260',  # Televisores LCD
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
                
                if not ntbkLinks:
                    break
                    
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

        return pageLinks

