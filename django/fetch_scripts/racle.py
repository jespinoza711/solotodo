#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Racle:
    name = 'Racle'
    
    # Main method
    def getNotebooks(self):
        print 'Getting Racle notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.racle.cl'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        urlWebpage = urlBase + '/ventas/tieda/notebook?limit=50&limitstart=0'            

        # Obtain and parse HTML information of the base webpage
        baseData = browser.open(urlWebpage).get_data()
        baseSoup = BeautifulSoup(baseData)

        # Obtain the links to the other pages of the catalog (2, 3, ...)
        productNames = baseSoup.findAll("a", { "class" : "producto_titulo" })
        productPrices = baseSoup.findAll("span", { "class" : "productPrice" })
        
        for i in range(len(productNames)):
            productData = ProductData()
            productData.custom_name = ' '.join(productNames[i].string.split())
            productData.url = urlBase + productNames[i]['href'].split('?')[0]
            productData.price = int(productPrices[i].string.replace('$', '').replace(' ', ''))
            productData.comparison_field = productData.url
            print productData
            productsData.append(productData)        
            
        return productsData

