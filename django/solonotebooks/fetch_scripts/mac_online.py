#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class MacOnline(FetchStore):
    name = 'MacOnline'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)

        product_name = product_soup.find('td', { 'class': 'tit_categoria_despliegue' }).contents[0].strip().encode('ascii', 'ignore')
        product_price = int(product_soup.find('em').string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.maconline.cl'
        urlBuscarProductos = '/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        product_links = []
        
        url_extensions = [  ['397.html', 'Notebook'],
                            ['421.html', 'Notebook'],
                            ['384.html', 'Notebook'],
                            ['288.html', 'Screen'],
                            ]
                            
        for url_extension, ptype in url_extensions:
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
                    
                    product_links.append([link, ptype])
                    
                page_number += 1

        return product_links

