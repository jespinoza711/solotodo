#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Magens:
    name = 'Magens'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        availability = product_soup.find('div', { 'class': 'stock' }).contents[4]
        if 'Agotado' in availability:
            return None
        
        product_name = product_soup.find('div', { 'class': 'titleContent' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('div', { 'class': 'precioDetalle' }).string.split('$')[1].replace(',', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting Magens notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.magens.cl'
        urlBuscarProductos = '/catalog/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  
            'notebooks-netbooks-netbooks-11-c-15_199.html',
            'notebooks-netbooks-notebooks-12-13-c-15_202.html',
            'notebooks-netbooks-notebooks-14-c-15_203.html',
            'notebooks-netbooks-notebooks-15-c-15_204.html',
            'notebooks-netbooks-notebooks-16-mas-c-15_205.html',
            'video-c-24_128.html',
            'video-pcie-c-24_130.html',
            'video-pcie-nvidia-c-24_129.html',
            'video-profesionales-c-24_131.html',
            'sam2-c-1_196.html',
            'sam3-c-1_31.html',
            'intel-s1156-c-1_197.html',
            'intel-s775-c-1_32.html',
            'server-c-1_30.html',
        ]
                
        product_links = []            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension + '?mostrar=100'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            nameDivs = baseSoup.findAll('div', { 'class': 'text11Red uppercase tituloProducto' })
            priceSpans = baseSoup.findAll('span', { 'class': 'text12Green' })[::2]
            for i in range(len(nameDivs)):
                link = nameDivs[i].find('a')
                product_links.append(link['href'].split('?osCsid')[0])
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

            
        return products_data

