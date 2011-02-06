#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Rigam:
    name = 'Rigam'

    # Main method
    def get_products(self):
        print 'Getting Rigam notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.rigam.cl/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'index.php?act=viewCat&catId=39&',
                            ]
                            
        for url_extension in url_extensions:
            page_number = 0
            
            while True:
                urlWebpage = urlBase + url_extension + 'page=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                products_table = baseSoup.find('table', { 'class' : 'tblList' })
                
                if not products_table:
                    break
                
                product_rows = products_table.findAll('tr')[1:]
                
                for product_row in product_rows:
                    link = product_row.find('a', { 'class' : 'txtDefault' })
                    url = urlBase + link['href']
                    name = link.find('strong').contents[0].encode('ascii', 'ignore')
                    price = product_row.find('span', { 'class' : 'txtOldPrice' }).contents[0]
                    price = int(price.replace('$', '').replace('.', ''))
                
                    product_data = ProductData()
                    product_data.custom_name = name
                    product_data.url = url
                    product_data.comparison_field = url
                    product_data.price = price
                    
                    print product_data
                    productsData.append(product_data)
                    
                page_number += 1
                
        return productsData

