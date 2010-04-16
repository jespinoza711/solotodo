#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class FullNotebook:
    name = 'FullNotebook'

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

	    productData.custom_name = title
	    productData.price = price
	    productData.url = productUrl

	    return productData


    # Main method
    def getNotebooks(self):
        print 'Getting FullNotebook notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.fullnotebook.cl/'
        urlBuscarProductos = 'tienda/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'mini-notebooks/page/',
                    'notebooks/page/',
                    'netbook/page/',
                    ]
        
        for url_extension in url_extensions:
        
            # Primero necesitamos el numero de paginas
            firstUrl = urlBase + urlBuscarProductos + url_extension + '1'
            baseData = browser.open(firstUrl).get_data()
            baseSoup = BeautifulSoup(baseData)
            listaPags = baseSoup.find("span", {'class': 'pages'})
            last_page = int(listaPags.contents[0][-1])
            
            for i in range(last_page):
                pageUrl = urlBase + urlBuscarProductos + url_extension + str(i + 1)            

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(pageUrl).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                prices = []
                names = []
                urls = []
                
                rawLinks = baseSoup.findAll("div", { 'class':'cliente'})
                for rawLink in rawLinks:
                    names.append(rawLink.find("a").string)
                    urls.append(rawLink.find("a")['href'])
                    
                rawPrices = baseSoup.findAll("span", { 'id':'prei'})
                for rawPrice in rawPrices:
                    price = (rawPrice.contents[0].replace("Precio:", '').replace('.', '').strip())
                    prices.append(int(price))
                    
                for j in range(len(names)):
                    productData = ProductData()
                    productData.custom_name = names[j].encode('ascii','ignore').strip()
                    productData.price = prices[j]
                    productData.url = urls[j]
                    print productData
                    productsData.append(productData)

        return productsData

