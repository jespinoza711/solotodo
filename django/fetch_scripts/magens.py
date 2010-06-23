#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Magens:
    name = 'Magens'

    # Method that extracts the data of a specific product given its page
    def retrieveProductsData(self, pageUrl):
        br = mechanize.Browser()
        data = br.open(pageUrl).get_data()
        soup = BeautifulSoup(data)

        productsData = []

        nameCells = soup.findAll("td", { "class" : "name name2_padd" })
        priceCells = soup.findAll("td", { "class" : "price2_padd" })
        
        for i in range(len(nameCells)):
            productData = ProductData()
            productData.custom_name = nameCells[i].find('a').string
            productData.url = nameCells[i].find('a')['href'].split('?osCsid')[0]
            productData.comparison_field = productData.url            
            productData.price = int(priceCells[i].contents[0].replace('Normal:', '').replace('$', '').replace(',', ''))
            print productData
            productsData.append(productData)


        return productsData


    # Main method
    def getNotebooks(self):
        print 'Getting Magens notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.magens.cl'
        urlBuscarProductos = '/catalog/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'notebooks-netbooks-netbooks-11-c-15_199.html',
                            'notebooks-netbooks-notebooks-12-13-c-15_202.html',
                            'notebooks-netbooks-notebooks-14-c-15_203.html',
                            'notebooks-netbooks-notebooks-15-c-15_204.html',
                            'notebooks-netbooks-notebooks-16-mas-c-15_205.html'
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            pageNavigator = baseSoup.find("td", { "class" : "result_right" })
            if not pageNavigator:
                continue
            relativePageLinks = pageNavigator.findAll('a')[:-1];

            # Array containing the catalog pages, beginning with the original one
            pageLinks = [urlWebpage]

            # Fix the relative links to the pages of the catalog and add the to the array
            for relativePageLink in relativePageLinks:
                pageLinks.append(relativePageLink['href'].split('&osCsid')[0])

            # Retrieve the data for each of the products and add it to the array
            for pageLink in pageLinks:
                prods = self.retrieveProductsData(pageLink)
                productsData += prods

        return productsData

