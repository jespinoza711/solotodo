#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Impulso:
    name = 'Impulso'


    def getNotebooks(self):
        print 'Getting Impulso notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://impulso.cl'
        urlBuscarProductos = '/prestashop/category.php?id_category='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '5',
                            '6',
                            '17',
                            '18',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            titles = baseSoup.findAll('h3')
            prices = baseSoup.findAll('span', {'class': 'price'})

            # Array containing the catalog pages, beginning with the original one
            pageLinks = [urlWebpage]

            for i in range(len(titles)):
                productData = ProductData()
                link = titles[i].find('a')
                productData.custom_name = link.string
                productData.url = link['href']
                productData.comparison_field = productData.url
                
                productData.price = int(prices[i + 1].string.replace('$', '').replace('.', ''))
                print productData
                productsData.append(productData)

        return productsData

