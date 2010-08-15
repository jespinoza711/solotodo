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
        urlBuscarProductos = '/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?papa=24&categoria=424',
                            '?papa=24&categoria=449',
                            '?papa=24&categoria=410',
                            '?papa=24&categoria=437',
                            '?papa=24&categoria=436'
                            ]
                          
        pageLinks = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            pageNumber = 1
                
            while True:
                completeWebpage = urlWebpage + '&pagina=' + str(pageNumber)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkLinks = baseSoup.findAll('a', { 'class' : 'vinculoNombreProd' })
                trigger = False
                for ntbkLink in ntbkLinks:
                    link = urlBase + ntbkLink['href']
                    if link in pageLinks:
                        trigger = True
                        break
                    pageLinks.append(link)
                    
                if trigger:
                    break
                    
                pageNumber += 1
                
        for link in pageLinks:
            baseData = browser.open(link).get_data()
            baseSoup = BeautifulSoup(baseData)
            productData = ProductData()
            titleSpan = baseSoup.find('span', { 'class' : 'productoFicha' })
            productData.custom_name = titleSpan.find('strong').string
            productData.url = link
            productData.comparison_field = link
            
            priceSpan = baseSoup.find('span', { 'id' : 'simulador' })
            productData.price = int(priceSpan.string.replace('.', ''))
            print productData
            productsData.append(productData)

        return productsData

