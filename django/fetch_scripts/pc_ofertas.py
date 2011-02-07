#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCOfertas:
    name = 'PC Ofertas'
    
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
        
        print product_data
        return product_data


    # Main method
    def getNotebooks(self):
        print 'Getting PC Ofertas notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcofertas.cl/index.php?route=product/category&path='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  '74',   # Notebook
                            '75',   # Netbook
                            ]
        
        product_links = []                    
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
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

