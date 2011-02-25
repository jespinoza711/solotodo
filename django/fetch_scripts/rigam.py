#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Rigam:
    name = 'Rigam'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('td', { 'class': 'cy2' }).find('strong').contents[0].encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'class': 'txtOldPrice' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Rigam notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.rigam.cl/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  'index.php?act=viewCat&catId=39',  # Notebooks
                            'index.php?act=viewCat&catId=60',   # Tarjetas de video
                            'index.php?act=viewCat&catId=40',   # Procesadores AMD
                            'index.php?act=viewCat&catId=2',    # Procesadores Intel
                            'index.php?act=viewCat&catId=54',   # Monitores
                            ]
        
        product_links = []                    
        for url_extension in url_extensions:
            page_number = 0
            
            while True:
                urlWebpage = urlBase + url_extension + '&page=' + str(page_number)

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
                    product_links.append(urlBase + link['href'])
                    
                page_number += 1
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

