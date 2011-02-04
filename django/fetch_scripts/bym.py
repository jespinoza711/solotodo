#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bym:
    name = 'Bym'

    # Main method
    def get_products(self):
        print 'Getting Bym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ttchile.cl/'
        urlBuscarProductos = 'subpro.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?idCat=21&idSubCat=20',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            
            productLinks = [div.find('a')['href'] for div in baseSoup.findAll('div', {'class': 'linkTitPro'})]
            
            for productLink in productLinks:
                urlProduct = urlBase + productLink
                
                baseData = browser.open(urlProduct).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                productData = ProductData()
                
                title = baseSoup.find('div', { 'class' : 'textTituloProducto'}).string.strip()
                
                prices = baseSoup.findAll('div', { 'class' : 'textOtrosPrecios' })
                price = prices[0].string
                price = int(price.replace('.', '').replace('$', ''))

                productData.custom_name = title
                productData.price = price
                productData.url = urlProduct.split('&osCsid')[0]
                productData.comparison_field = productData.url	    	    
                productsData.append(productData)
                
                print productData

        return productsData

