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
                            ['?papa=24&categoria=424', 'Notebook'],   # Notebooks 7 a 11
                            ['?papa=24&categoria=449', 'Notebook'],   # Notebooks 12 a 13
                            ['?papa=24&categoria=410', 'Notebook'],   # Notebooks 14
                            ['?papa=24&categoria=437', 'Notebook'],   # Notebooks 15
                            ['?papa=24&categoria=436', 'Notebook'],   # Notebooks 16 y +
                            ['?papa=334&categoria=40', 'VideoCard'],   # VGA AGP
                            ['?papa=334&categoria=378', 'VideoCard'],  # VGA PCIe Nvidia
                            ['?papa=334&categoria=454', 'VideoCard'],  # VGA PCIe ATI
                            ['?papa=334&categoria=455', 'VideoCard'],  # VGA Profesionales
                            ['?papa=272&categoria=409', 'Processor'],  # CPU Server
                            ['?papa=272&categoria=465', 'Processor'],  # CPU AM3
                            ['?papa=272&categoria=388', 'Processor'],  # CPU 775
                            ['?papa=272&categoria=468', 'Processor'],  # CPU 1156
                            ['?papa=272&categoria=446', 'Processor'],  # CPU 1366
                            ['?papa=256&categoria=250', 'Screen'],  # Monitores LCD
                            ['?papa=256&categoria=260', 'Screen'],  # Televisores LCD
                            ['?papa=292&categoria=473', 'Motherboard'],  # MB AM3
                            ['?papa=292&categoria=392', 'Motherboard'],  # MB 775
                            ['?papa=292&categoria=467', 'Motherboard'],  # MB 1156
                            ['?papa=292&categoria=447', 'Motherboard'],  # MB 1366
                            ]
                          
        products_data = []                      
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            
            soup = BeautifulSoup(browser.open(urlWebpage).get_data())
            
            try:
                page_count = int(soup.findAll('table', {'class': 'descripcionbold'})[1].findAll('td', {'align': 'center'})[-1].find('a').string)
            except:
                page_count = 1
            
            product_links = []
                
            for page in range(page_count):
                page += 1
                
                completeWebpage = urlWebpage + '&pagina=' + str(page)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkLinks = baseSoup.findAll('a', { 'class' : 'vinculoNombreProd' })
                    
                for ntbkLink in ntbkLinks:
                    link = urlBase + ntbkLink['href']
                    link = link.encode('ascii', 'ignore')
                    if link not in product_links:
                        product_links.append(link)
                
            for link in product_links:
                products_data.append([link, ptype])

        return products_data

