#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Webco:
    name = 'Webco'

    # Main method
    def getNotebooks(self):
        print 'Getting Webco notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www1.webco.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'n_new_productos.asp?CATEGORIA={761FD739-2D0F-4177-8AE0-C641D6F16502}',
                            'n_new_productos.asp?CATEGORIA={D70BBB30-F5E9-4246-B812-A939C8777429}',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            
            baseSoup = BeautifulSoup(baseData)

            # Obtain a reference tag for each product (in this case it image)
            productImages = baseSoup.findAll("img", { "width" : "193" })
            
            for productImage in productImages:
                productData = ProductData()
                productData.url = urlBase + productImage.parent['href']
                productData.custom_name = productImage.parent.parent.parent.parent.find('strong').string.encode('ascii','ignore').strip()
                productData.price = int(productImage.parent.parent.parent.parent.find("td", { "class" : "precio" }).find('a').string.replace('$', '').replace('-', '').replace('.', '').strip())
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)
        return productsData

