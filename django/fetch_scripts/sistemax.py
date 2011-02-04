#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Sistemax:
    name = 'Sistemax'

    # Main method
    def get_products(self):
        print 'Getting Sistemax notebooks'
        # Basic data of the target webpage and the specific catalog
        baseUrl = 'http://www.sistemax.cl/webstore/'
        
        extensions = ['index.php?op=seccion/id=112&page=-1&listar=true',
                        'index.php?op=seccion/id=27&page=-1&listar=true' ]
                        
        # Array containing the data for each product
        productsData = []
                        
        for extension in extensions:
        
            urlWebpage = baseUrl + extension
            
            # Browser initialization
            browser = mechanize.Browser()

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            info_cells = baseSoup.findAll("td", { 'scope' : 'col'})

            name_cells = info_cells[::5]
            names = [name_cell.contents[0].string for name_cell in name_cells]
            
            price_cells = info_cells[1::5]
            prices = [int(price_cell.contents[0].string) for price_cell in price_cells]
            
            url_cells = info_cells[3::5]
            urls = [baseUrl + url_cell.contents[2]['href'] for url_cell in url_cells]
            
            for i in range(len(name_cells)):
                productData = ProductData()
                productData.custom_name = names[i].encode('ascii', 'ignore')
                productData.price = prices[i]
                productData.url = urls[i]
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)
                
        return productsData

