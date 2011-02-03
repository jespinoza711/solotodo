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
        
        urlSearch = '/ventas/tienda/'            

        urlExtensions = ['netbook', 'notebook']

        for urlExtension in urlExtensions:
            urlWebpage = urlBase + urlSearch + urlExtension + '?limit=50&limitstart=0'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productDetailsCells = baseSoup.findAll('td', { 'class' : 'producto_fondo_tabla_M' })
            
            for productDetailCell in productDetailsCells:
                productLink = productDetailCell.find('a', { 'class' : 'producto_titulo' })
                productPriceSpan = productDetailCell.find('span', { 'class' : 'productPrice' })
                
                if not productPriceSpan:
                    continue
            
                productData = ProductData()
                productData.custom_name = ' '.join(productLink.string.split())
                productData.url = urlBase + productLink['href'].split('?')[0]
                productData.price = int(productPriceSpan.string.replace('$', '').replace(' ', ''))
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)        
            
        return productsData

