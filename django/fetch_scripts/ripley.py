#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Ripley:
    name = 'Ripley'

    # Main method
    def getNotebooks(self):
        print 'Getting Ripley notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ripley.cl'
        urlBuscarProductos = '/webapp/wcs/stores/servlet/CategoryDisplay?catalogId=10051&storeId=10051&categoryId=57103&langId=-1&curPg='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        j = 1                    
        while True:
            urlWebpage = urlBase + urlBuscarProductos + str(j)

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productParagraphs = baseSoup.findAll("p", { "onmouseover" : "" })
            productPrices = baseSoup.findAll("span", { "class" : "normalHOME" })
            
            productLinks = []
            for productPrice in productPrices:
                notebookCell = productPrice.parent.parent.parent.parent
                link = notebookCell.find('a')['href']
                productLinks.append('http://www.ripley.cl/webapp/wcs/stores/servlet/' + link)
            
            productPrices = [int(price.string.replace('.', '').replace('$', '')) for price in productPrices]
            
            productNames = [p.contents[0].strip() + ' ' + p.contents[2].replace('&nbsp;', '').strip() for p in productParagraphs]
           
            if len(productParagraphs) == 0:
                break
            for i in range(len(productNames)):
                productData = ProductData()
                productData.custom_name = productNames[i]
                productData.price = productPrices[i]
                productData.url = productLinks[i]
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)
            j += 1
        return productsData
