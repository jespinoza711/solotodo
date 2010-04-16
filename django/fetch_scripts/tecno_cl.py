#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class TecnoCl:
    name = 'Tecno.cl'

    # Main method
    def getNotebooks(self):
        print 'Getting Tecno.cl notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecno.cl/'
        urlBuscarProductos = 'prod/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'productos.asp?cat=8',
                            'productos.asp?cat=259',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawProductLinks = baseSoup.findAll("a", { "class" : "txtchico" })
            
            productLinks = []
            productNames = []
            
            for rawProductLink in rawProductLinks:
                productLinks.append(urlBase + urlBuscarProductos + rawProductLink['href'])
                rawComponents = rawProductLink.contents[0].contents
                name_1 = rawComponents[1].contents[0]
                name_2 = rawComponents[2].contents[0][2::].strip()
                productNames.append(name_1 + ' ' + name_2)
                
            productPrices = []
            rawProductPrices = baseSoup.findAll("span", { "class" : "vtrtit" })            
            for rawProductPrice in rawProductPrices:
                stringPrice = rawProductPrice.contents[0].replace('Normal', '').replace('$', '').replace('.', '').replace('iva Inc', '').strip()
                if stringPrice == 'Contado':
                    continue
                else:
                    productPrices.append(int(stringPrice))
                    
            for i in range(len(productNames)):
                productData = ProductData()
                productData.custom_name = productNames[i]
                productData.url = productLinks[i]
                productData.price = productPrices[i]
                print productData
                productsData.append(productData)

        return productsData

