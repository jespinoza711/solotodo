#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Sistemax:
    name = 'Sistemax'
    
    def retrieve_product_data(self, product_link):
        print product_link
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.findAll('h2')[3].find('font').string.encode('ascii', 'ignore')
        product_price = int(product_soup.findAll('span', { 'class': 'style18' })[1].string)
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Sistemax notebooks'
        # Basic data of the target webpage and the specific catalog
        baseUrl = 'http://www.sistemax.cl/webstore/'
        url_buscar_productos = 'index.php?op=seccion/id='
        
        extensions = [
                # Netbooks
                '112',
                # Notebooks
                '27', 
                ]
                        
        # Array containing the data for each product
        products_data = []
        product_links = []                
        for extension in extensions:
            urlWebpage = baseUrl + url_buscar_productos + extension + '&page=-1&listar=true'
            
            browser = mechanize.Browser()

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            info_cells = baseSoup.findAll("td", { 'scope' : 'col'})
            
            url_cells = info_cells[3::5]
            urls = [baseUrl + url_cell.contents[2]['href'] for url_cell in url_cells]
            product_links.extend(urls)
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

