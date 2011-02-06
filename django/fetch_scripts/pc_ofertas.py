#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCOfertas:
    name = 'PC Ofertas'

    # Main method
    def get_products(self):
        print 'Getting PC Ofertas notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcofertas.cl/index.php?route=product/category&path='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '74',
                            '75'
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
                link = link[1]
                url = link['href']
                name = link.contents[0]
                price_span = product_cell.findAll('span')[1]
                price = int(price_span.contents[0].replace('$', '').replace(',', ''))
                
                product_data = ProductData()
                product_data.custom_name = name
                product_data.url = url
                product_data.comparison_field = url
                product_data.price = price
                
                print product_data
                
                productsData.append(product_data)

        return productsData

