#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Peta:
    name = 'Peta'

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
        productData.url = productUrli
        productData.comparison_field = productData.url

        return productData


    # Main method
    def getNotebooks(self):
        print 'Getting Peta notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.peta.cl'
        urlBuscarProductos = '/computadores-1/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'netbooks.html',
                            'notebooks.html',
                            ]
                          
        pageLinks = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            pageNumber = 1
                
            while True:
                completeWebpage = urlWebpage + '?p=' + str(pageNumber)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkCells = baseSoup.find('table', { 'id': 'product-list-table'}).findAll('td')
                

                trigger = False
                for ntbkCell in ntbkCells:
                    try:
                        link = ntbkCell.findAll('a')[1]
                    except:
                        break
                    if link['href'] in pageLinks:
                        trigger = True
                        break
                    productData = ProductData()
                    productData.url = link['href']
                    productData.custom_name = link.string.encode('ascii', 'ignore')
                    productData.comparison_field = link['href']
                    productData.price = int(ntbkCell.find('span', {'class': 'price'}).string.replace('.', '').replace('$', ''))
                    productsData.append(productData)
                    print productData
                    pageLinks.append(link['href'])
                    
                if trigger:
                    break
                    
                pageNumber += 1
                
        return productsData

