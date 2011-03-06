#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PCOfertas(FetchStore):
    name = 'PC Ofertas'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        
        product_name = product_soup.find('h4', { 'class': 'Estilo5' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'class': 'Estilo4' }).parent.parent.parent.findAll('td')[3].find('span').string.replace('$', '').replace(',', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcofertas.cl/index.php?route=product/category&path='
        
        # Browser initialization
        browser = mechanize.Browser()
        product_links = []
        
        url_extensions = [  '74',   # Notebook
                            '75',   # Netbook
                            '87',   # Tarjetas de video
                            '18',   # Procesadores
                            '28',   # Monitores
                            ]
        
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            products_table = baseSoup.findAll('table', { 'class' : 'list' })[-1]
            
            product_cells = products_table.findAll('td')
            
            for product_cell in product_cells:
                link = product_cell.findAll('a')
                if not link:
                    break
                product_links.append(link[1]['href'])

        return product_links

