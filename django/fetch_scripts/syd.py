#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Syd:
    name = 'Syd'

    # Main method
    def getNotebooks(self):
        print 'Getting Syd notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.syd.cl'
        urlBuscarProductos = '/computadoras/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'macbook_pro/?op=all&crit=',
                            'macbook/?op=all&crit=',
                            'macbook_air/?op=all&crit=',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            titles = baseSoup.findAll('h4')
            prices = baseSoup.findAll('dl', { 'class' : 'precios' })

            for i in range(len(titles)):
                productData = ProductData()
                link = titles[i].find('a')
                productData.custom_name = link.string
                productData.url = link['href']
                productData.comparison_field = productData.url

                priceLinks = prices[i].findAll('a')
                priceLink = priceLinks[len(priceLinks) - 1]
                productData.price = int(priceLink.string.replace('$', '').replace('.', ''))
                print productData
                productsData.append(productData)
			
        return productsData

