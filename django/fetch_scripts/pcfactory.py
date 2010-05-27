#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCFactory:
    name = 'PCFactory'

    # Method that extracts the <a> tags to products given the URL of the catalog page
    def extractLinks(self, pageUrl):
	    br = mechanize.Browser()
	    data = br.open(pageUrl).get_data()
	    soup = BeautifulSoup(data)
	    links = soup.findAll("a", { "class" : "linkProducto" })

	    return links

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()

        titleSpan = soup.find("span", { "class" : "style22" })
        title = str(titleSpan.string).strip()

        priceCell = soup.findAll("td", { "class" : "productoiva" })
        price = int(str(priceCell[1].string).replace('.', ''))

        productData.custom_name = titleSpan.string.strip()
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url

        return productData


    # Main method
    def getNotebooks(self):
        print 'Getting PCFactory notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcfactory.cl'
        urlBuscarProductos = '/buscar_productos.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?sc=-24&g=424',
                            '?sc=-24&g=449',
                            '?sc=-24&g=410',
                            '?sc=-24&g=437',
                            '?sc=-24&g=436'
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            pageNavigator = baseSoup.find("span", { "class" : "textproductos" })
            relativePageLinks = pageNavigator.findAll('a')[1:-1];

            # Array containing the catalog pages, beginning with the original one
            pageLinks = [urlWebpage]

            # Fix the relative links to the pages of the catalog and add the to the array
            for relativePageLink in relativePageLinks:
                pageLinks.append(urlBase + urlBuscarProductos + relativePageLink['href'])

            # Array containing the links to the specific products
            productLinks = []

            # For each of the pages, retrieve the fixed links to the products and add them to the array
            for pageLink in pageLinks:
                rawLinks = self.extractLinks(pageLink)
                for rawLink in rawLinks:
	                productLinks.append(urlBase + rawLink['href'])

            # Retrieve the data for each of the products and add it to the array
            for productLink in productLinks:
                try:
                    prod = self.retrieveProductData(productLink)
                except:
                    print 'Error ' + productLink
                    continue
                print prod
                productsData.append(prod)

        return productsData

