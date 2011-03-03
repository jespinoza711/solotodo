#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class Compumanque:
    name = 'Compumanque'

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        title = soup.find('h1').string
        
        price = int(soup.findAll('b')[1].parent.parent.findAll('td')[1].string.replace('$', '').replace('.', ''))
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        print productData
        return productData


    # Main method
    def get_products(self):
        print 'Getting Compumanque notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://72.249.5.151/~compucl/index.php?route=product/category&path='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '101_87',    # Tarjetas de video
                            '19',     # Procesadores
                            '45_97',    # Monitores
                            '45_98',    # TV
                            '106',   # Netbooks
                            '50',     # Notebooks
                            ]
                            
        productLinks = []
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData).find('table', { 'class' : 'list' })
            
            if not baseSoup:
                continue

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawLinks = baseSoup.findAll('a')[::2]
            
            for rawLink in rawLinks:
                link = rawLink['href']
                productLinks.append(link)
                    
        for productLink in productLinks:
            prod = self.retrieve_product_data(productLink)
            if prod:
                productsData.append(prod)

        return productsData

