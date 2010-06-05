#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class GlobalMac:
    name = 'GlobalMac'

    # Main method
    def getNotebooks(self):
        print 'Getting GlobalMac notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.globalmac.cl/'
        urlBuscarProductos = 'ver=Apple/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'MacBook',
                            'MacBook%20Pro',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            
            titles = baseSoup.findAll('h3')
            prices = baseSoup.findAll('div', {'class': 'price'})

            # Fix the relative links to the pages of the catalog and add the to the array
            dephase = 0
            for i in range(len(titles)):
                productData = ProductData()
                link = titles[i].find('a')
                
                if link == None:
                	dephase += 1
                	continue
                
                productData.custom_name = link.string
                productData.url = urlBase + link['href']
                productData.comparison_field = productData.url
                
                productData.price = int(prices[i - dephase].find('h4').string.replace('Precio', '').replace('$', '').replace('.', ''))
                print productData
                productsData.append(productData)
                

        return productsData

