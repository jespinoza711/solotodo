#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PortatilChile:
    name = 'PortatilChile'

    # Main method
    def getNotebooks(self):
        print 'Getting PortatilChile notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.portatilchile.cl/modules/rmms/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        baseData = browser.open(urlBase).get_data()
        baseSoup = BeautifulSoup(baseData)
        
        productTable = baseSoup.find('table', { 'class': 'outer' })
        productRows = productTable.findAll('tr', recursive = False)
        productCells = []
        for productRow in productRows:
            productCells.extend(productRow.findAll('td', recursive = False))
        
        # Array containing the data for each product
        productsData = []
        
        for productCell in productCells:
            productLink = productCell.find('a')
            
            productData = ProductData()
            productData.custom_name = productLink['title']
            productData.url = urlBase + productLink['href']
            productData.comparison_field = productData.url
            priceData = productCell.findAll('strong')[1].text
            productData.price = int(priceData.replace('.', '').replace('$', ''))
            print productData

        return productsData

