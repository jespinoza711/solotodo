#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PackardBell:
    name = 'Packard Bell'

    # Main method
    def get_products(self):
        print 'Getting Packard Bell notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.packardbell.cl'
        urlCatalog = '/2010/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'index.php?seccion=productos&idCategoria=112',
                            'index.php?seccion=productos&idCategoria=116'
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlCatalog + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            nameDivTags = baseSoup.findAll('div', { 'class' : 'nombre_prod' })
            priceDivTags = baseSoup.findAll('div', { 'class' : 'precio_prod' })
            imgTags = baseSoup.findAll('div', { 'class' : 'img_prod' })            
            
            for i in range(len(nameDivTags)):
                productData = ProductData()
                productData.url = imgTags[i]['onclick'].replace('javascript:location.href=\'', '').replace('\'', '')
                productData.custom_name = nameDivTags[i].string
                productData.price = int(priceDivTags[i].contents[0].replace('.', ''))
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)
                
        return productsData

