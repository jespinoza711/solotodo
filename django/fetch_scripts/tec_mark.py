#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class TecMark:
    name = 'TecMark'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
	    br = mechanize.Browser()
	    data = br.open(productUrl).get_data()
	    soup = BeautifulSoup(data)

	    productData = ProductData()

	    titleSpan = soup.findAll("strong")
	    if len(titleSpan) == 6:
	        return None
	        
	    titleTable = soup.find("table", { "bordercolor" : "#C0C0C0" })
	    title = titleTable.find("b").string
	    title = title.encode('ascii','ignore').strip()
	    
	    priceString = titleSpan[14].find("font").string.replace('$', '').replace('.', '').strip()
	    price = int(priceString)
	    productData.custom_name = title
	    productData.price = price
	    productData.url = productUrl
	    
	    print productData
	    
	    return productData


    # Main method
    def getNotebooks(self):
        print 'Getting TecMark notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecmark.cl/'
        preUrl = 'index.php?smenu=Tienda&c_familia=20&n_pag='
        postUrl = '&n_pag_total=4'
        urlBuscarProductos = '/buscar_productos.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
                            
        for i in range(4):
            urlWebpage = urlBase + preUrl + str(i + 1) + postUrl
            print urlWebpage

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            pageNavigator = baseSoup.find("td", { "id" : "contentBody" }).contents
            
            rawTables = pageNavigator[2].contents[5:-1]
            
            
            productLinks = []
            for rawTable in rawTables:
                links = rawTable.findAll("a")
                links = links[::2]
                for link in links:
                    productLinks.append(urlBase + link['href'])

            # Retrieve the data for each of the products and add it to the array
            for productLink in productLinks:
                pd = self.retrieveProductData(productLink)
                if pd:
                    productsData.append(pd)

        return productsData

