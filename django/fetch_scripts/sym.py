#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Sym:
    name = 'Sym'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()

        titleSpan = soup.find("h1")
        title = str(titleSpan.string).strip()
        try:
            priceCell = soup.find("div", { "id" : "product-info" }).find("ul").findAll("li")[1].contents[1]
            price = int(str(priceCell.replace('.', '').replace('$', '')))
        except:
            priceCell = soup.find("div", { "id" : "product-info" }).find("ul").findAll("li")[2].contents[1]
            price = int(str(priceCell.replace('.', '').replace('$', '')))

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url

        return productData


    # Main method
    def getNotebooks(self):
        print 'Getting Sym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.sym.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?cat=104',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawLinks = baseSoup.findAll("div", { "class" : "listadoindiv" })
            
            productLinks = []
            for rawLink in rawLinks:
                productLinks.append(rawLink.find("h2").find("a")['href'])
                
                
            for productLink in productLinks:
                prod = self.retrieveProductData(productLink)
                print prod
                productsData.append(prod)

        return productsData

