#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class MacOnline:
    name = 'MacOnline'

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
        print 'Getting MacOnline notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.maconline.cl'
        urlBuscarProductos = '/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '178-MacBook.html',
                            '179-MacBook%20Pro.html',
                            '350-MacBook%20Pro%20(New).html',
                            '190-MacBook%20Air.html',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            titles = baseSoup.findAll('td', { 'class' : 'nombre_producto' })
            prices = baseSoup.findAll('td', { 'class' : 'precio_producto' })

            for i in range(len(titles)):
                productData = ProductData()
                link = titles[i].find('a')
                productData.custom_name = link.string
                productData.url = urlBase + link['href']
                productData.comparison_field = productData.url
                
                productData.price = int(prices[i].string.replace('$', '').replace('.', ''))
                print productData
                productsData.append(productData)

        return productsData

