#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class TopPC:
    name = 'TopPC'

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        title = soup.find('h2').string
        
        price = int(soup.find('span', { 'id': 'old_price_display' }).string.replace('$', '').replace('.', ''))
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        print productData
        return productData


    # Main method
    def get_products(self):
        print 'Getting TopPC notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.toppc.cl/beta/category.php?n=50&id_category='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '76',    # Tarjetas de video
                            '5',     # Procesadores
                            '61',    # Monitores y TV
                            ]
                            
        productLinks = []
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawLinks = baseSoup.findAll('a', { 'class' : 'product_img_link' })
            
            for rawLink in rawLinks:
                link = rawLink['href']
                productLinks.append(link)
                    
        for productLink in productLinks:
            prod = self.retrieve_product_data(productLink)
            if prod:
                productsData.append(prod)

        return productsData

