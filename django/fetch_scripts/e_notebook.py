#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class ENotebook:
    name = 'E-Notebook'
    
    # Method that extracts the product details from a given page
    def extractProducts(self, pageUrl):
        br = mechanize.Browser()
        data = br.open(pageUrl).get_data()
        soup = BeautifulSoup(data)
        products = []
        cellis = soup.findAll("td", { "class" : "productListing-data" })
        cells = cellis[1::4]
        prices = cellis[2::4]
        for i in range(len(cells)):
            productData = ProductData()
            link = cells[i].find("a")
            productData.url = link['href'].split('?osCsid')[0]
            productData.custom_name = link.string
            productData.comparison_field = productData.url
            priceCell = prices[i]
            specContainer = priceCell.find("span", { "class" : "productSpecialPrice" })
            if (not specContainer):
                priceTag = priceCell.string.replace('.', '').replace('$', '').replace('&nbsp;', '').strip()
                productData.price = int(int(priceTag) * 1.07)
            else:
                priceTag = specContainer.string.replace('.', '').replace('$', '').strip()
                productData.price = int(int(priceTag) * 1.07)
            print productData
            products.append(productData)    
        return products

    # Method that extracts the products from a given catalog page
    def extractLinks(self, pageUrl):
        br = mechanize.Browser()
        data = br.open(pageUrl).get_data()
        soup = BeautifulSoup(data)
        links = [pageUrl];
        pageLinks = soup.findAll("a", { "class" : "pageResults" })[:-1]
        for pageLink in pageLinks:
            links.append(pageLink['href'])
            
        products = []
        for link in links:
            products += self.extractProducts(link)
        return products

    # Main method
    def get_products(self):
        print 'Getting E-Notebook notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.notebook.cl/'
        urlBuscarProductos = 'venta/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        urlWebpage = urlBase + urlBuscarProductos + 'it-index-n-notebooks-cP-1.html'

        # Obtain and parse HTML information of the base webpage
        baseData = browser.open(urlWebpage).get_data()
        baseSoup = BeautifulSoup(baseData)
        
        # Array containing the catalog pages, beginning with the original one
        pageLinks = []

        # Obtain the links to the other pages of the catalog (2, 3, ...)
        pageNavigator = baseSoup.findAll("td", { "class" : "smallText" })
        pageNavigator = pageNavigator[:8]
        for pn in pageNavigator:
            link = pn.find("a")
            pageLinks.append(link['href'])

        # Array containing the links to the specific products
        productLinks = []

        # For each of the pages, retrieve the data of the products
        for pageLink in pageLinks:
            products = self.extractLinks(pageLink)
            for product in products:
                productsData.append(product)
        return productsData

