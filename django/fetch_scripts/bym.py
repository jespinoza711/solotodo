#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bym:
    name = 'Bym'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
	    br = mechanize.Browser()
	    data = br.open(productUrl).get_data()
	    soup = BeautifulSoup(data)

	    productData = ProductData()

	    titleSpan = soup.find("td", { "class" : "pageHeading" })
	    title = str(titleSpan.string).strip()

	    priceCell = soup.findAll("td", { "class" : "main" })[1]
	    price = int(str(priceCell.find("strong").string.replace('.', '').replace('$', '')))

	    productData.custom_name = title
	    productData.price = price
	    productData.url = productUrl
	    productData.comparison_field = productData.url	    	    
	    
	    print productData

	    return productData


    # Main method
    def getNotebooks(self):
        print 'Getting Bym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.bymcomputer.cl'
        urlBuscarProductos = '/catalog/index.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?cPath=84_147',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawLinks = baseSoup.findAll("td", { "class" : "productListing-data" })
            rawLinks = rawLinks[2::5]
            
            productLinks = []
            for rawLink in rawLinks:
                productLinks.append(rawLink.find("a")['href'])
                
                
            for productLink in productLinks:
                prod = self.retrieveProductData(productLink)
                productsData.append(prod)

        return productsData

