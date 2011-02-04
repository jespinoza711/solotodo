#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class TecnoGroup:
    name = 'TecnoGroup'

    # Main method
    def get_products(self):
        print 'Getting TecnoGroup notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecnogroup.cl/'
        urlBuscarProductos = 'index.php?cPath='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
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
                
                productData = ProductData()
                
                url = nameLink['href']
                i = url.find('&osCsid')
                if i != -1:
                    url = url[:i]
                productData.custom_name = nameLink.string
                productData.url = url
                productData.comparison_field = productData.url
                productData.price = int(priceSpan.string.replace('$', '').replace('.', ''))
                print productData
                
                productsData.append(productData)
                
        return productsData

