#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class TecnoGroup:
    name = 'TecnoGroup'
    
    def retrieve_product_data(self, product_link):
        print product_link
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h3').contents[0]
        product_price = int(product_soup.find('h3').parent.findAll('div')[3].string.split('$')[1].split('IVA')[0].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting TecnoGroup notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecnogroup.cl/'
        urlBuscarProductos = 'index.php?cPath='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  '2_35',
                            '2_81',
                            '2_117',
                            '2_33',
                            '2_43',
                            '2_10',
                            '2_11',
                            '2_13',
                            '2_34',
                            '4_44',
                            '4_139',
                            '4_47',
                            '4_48',
                            '4_49',
                            '4_109',
                            '4_45',
                            '4_46',
                            ]
        
        product_links = []                  
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData).find('td', {'class':'tableBox_output_td main'})
            
            try:
                nameCells = baseSoup.findAll('td', {'class': 'name name2_padd'})
            except:
                continue
            priceSpans = baseSoup.findAll('span', {'class': 'productSpecialPrice'})
            
            for i in range(len(nameCells)):
                nameLink = nameCells[i].find('a')
                priceSpan = priceSpans[i]

                url = nameLink['href'].split('&osCsid')[0]
                product_links.append(url)
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data


