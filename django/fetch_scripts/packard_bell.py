#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PackardBell:
    name = 'Packard Bell'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
	    br = mechanize.Browser()
	    data = br.open(productUrl).get_data()
	    soup = BeautifulSoup(data)

	    productData = ProductData()

	    titleSpan = soup.find("h1")
	    title = str(titleSpan.string).strip()

	    priceCell = soup.find("div", { "id" : "product-info" }).find("ul").findAll("li")[1].contents[1]
	    price = int(str(priceCell.replace('.', '').replace('$', '')))

	    productData.custom_name = title
	    productData.price = price
	    productData.url = productUrl

	    return productData


    # Main method
    def getNotebooks(self):
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
            
            for i in range(len(nameDivTags)):
                productData = ProductData()
                productData.url = urlWebpage
                productData.custom_name = nameDivTags[i].string
                productData.price = int(priceDivTags[i].contents[0].replace('.', ''))
                print productData
                productsData.append(productData)
                
        return productsData

