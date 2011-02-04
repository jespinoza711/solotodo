#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Peta:
    name = 'Peta'

    # Main method
    def get_products(self):
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

                ntbkCells = baseSoup.find('table', { 'id': 'product-list-table'})
                if not ntbkCells:
                    break
                
                ntbkCells = ntbkCells.findAll('td')
                

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

