#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Magens(FetchStore):
    name = 'Magens'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except: 
            return None
        product_soup = BeautifulSoup(product_data)
        
        availability = product_soup.find('div', { 'class': 'stock' }).contents[4]
        if 'Agotado' in availability:
            return None
        
        product_name = product_soup.find('div', { 'class': 'titleContent' }).string.encode('ascii', 'ignore')
        try:
            product_price = int(product_soup.findAll('div', { 'class': 'precioDetalle' })[1].string.split('$')[1].replace(',', ''))
        except:
            product_price = int(product_soup.findAll('div', { 'class': 'precioDetalle' })[0].string.split('$')[1].replace(',', ''))
        part_number = product_soup.find('div', { 'class': 'codProduct' }).string.replace('[', '').replace(']', '').encode('ascii', 'ignore').strip()
        part_number = product_soup.find('div', { 'class': 'codProduct' }).string.replace('[', '').replace(']', '').encode('ascii', 'ignore').strip()
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        product_data.part_number = part_number
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.magens.cl'
        urlBuscarProductos = '/catalog/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  
            ['notebooks-netbooks-netbooks-11-c-15_199.html', 'Notebook'], 
            ['notebooks-netbooks-notebooks-12-13-c-15_202.html', 'Notebook'], 
            ['notebooks-netbooks-notebooks-14-c-15_203.html', 'Notebook'], 
            ['notebooks-netbooks-notebooks-15-c-15_204.html', 'Notebook'], 
            ['notebooks-netbooks-notebooks-16-mas-c-15_205.html', 'Notebook'], 
            ['video-c-24_128.html', 'VideoCard'], 
            ['video-pcie-c-24_130.html', 'VideoCard'], 
            ['video-pcie-nvidia-c-24_129.html', 'VideoCard'], 
            ['video-profesionales-c-24_131.html', 'VideoCard'], 
            ['sam2-c-1_196.html', 'Processor'], 
            ['sam3-c-1_31.html', 'Processor'], 
            ['intel-s1156-c-1_197.html', 'Processor'], 
            ['intel-s775-c-1_32.html', 'Processor'], 
            ['server-c-1_30.html', 'Processor'], 
            ['monitores-televisores-c-13.html', 'Screen'], 
            ['placas-madre-c-2.html', 'Motherboard'], 
        ]
                
        product_links = []            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension + '?mostrar=100'
            
            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            nameDivs = baseSoup.findAll('div', { 'class': 'text11 uppercase tituloProducto' })
            for i in range(len(nameDivs)):
                link = nameDivs[i].find('a')['href']
                product_links.append([link.split('?osCsid')[0], ptype])
            
        return product_links

