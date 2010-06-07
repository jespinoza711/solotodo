#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class RkNotebooks:
    name = 'rK-Notebooks'

    # Main method
    def getNotebooks(self):
        print 'Getting RkNotebooks notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.rk-notebooks.cl'
        urlBuscarProductos = '/store/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extension = 'category.php?id_category=7'
                            
        urlWebpage = urlBase + urlBuscarProductos + url_extension

        baseData = browser.open(urlWebpage).get_data()
        baseSoup = BeautifulSoup(baseData)

        titles = baseSoup.findAll('h3')
        prices = baseSoup.findAll('span', {'class': 'price'})

        for i in range(len(titles)):
            productData = ProductData()
            link = titles[i].find('a')
            productData.custom_name = link.string
            productData.url = link['href']
            productData.comparison_field = productData.url
            
            productData.price = int(prices[i].string.replace('$', '').replace('.', ''))
            print productData
            productsData.append(productData)
        
        return productsData

