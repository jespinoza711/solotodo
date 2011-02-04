#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bip:
    name = 'Bip'

    # Method that extracts the <a> tags to products given the URL of the catalog page
    def extractLinks(self, pageUrl):
	    br = mechanize.Browser()
	    data = br.open(pageUrl).get_data()
	    soup = BeautifulSoup(data)
	    links = soup.findAll("a", { "class" : "menuprod" })
	    links = links[::2]

	    return links

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
	    br = mechanize.Browser()
	    data = br.open(productUrl).get_data()
	    soup = BeautifulSoup(data)

	    productData = ProductData()

	    titleSpan = soup.find("td", { "class" : "menuprodg" })
	    title = titleSpan.string.strip()

	    priceCell = soup.findAll("td", { "class" : "prc8" })
	    price = int(str(priceCell[1].string).replace('.', '').replace('$', '').strip())

	    productData.custom_name = title.encode('ascii','ignore').strip()
	    productData.price = price
	    productData.url = productUrl
	    productData.comparison_field = productData.url	    
	    
	    print productData

	    return productData


    # Main method
    def get_products(self):
        print 'Getting Bip notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.bip.cl/ecommerce/'
        urlBuscarProductos = 'index.php?modulo=busca&'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'categoria=229&categoria_papa=191',
                            'categoria=167&categoria_papa=166',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            pageLinks = [urlWebpage]
            rawPageLinks = baseSoup.findAll("a", { "class" : "pag" })
            rawPageLinks = rawPageLinks[:len(rawPageLinks) / 2]
            
            for rawPageLink in rawPageLinks:
                pageLinks.append(urlBase + rawPageLink['href'])

            
            # Array containing the links to the specific products
            productLinks = []
            
            # For each of the pages, retrieve the fixed links to the products and add them to the array
            for pageLink in pageLinks:
                rawLinks = self.extractLinks(pageLink)
                for rawLink in rawLinks:
	                productLinks.append(urlBase + rawLink['href'])
            
            # Retrieve the data for each of the products and add it to the array
            for productLink in productLinks:
                prod = self.retrieveProductData(productLink)
                productsData.append(prod)
            

        return productsData

