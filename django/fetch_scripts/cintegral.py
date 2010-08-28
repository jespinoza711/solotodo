#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Cintegral:
    name = 'Cintegral'

    # Main method
    def getNotebooks(self):
        print 'Getting Cintegral notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://cintegral.cl'
        urlBuscarProductos = '/index.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?op=cat&id=84',
                            '?op=cat&id=9', ]
                          
        pageLinks = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            pageNumber = 1
                
            while True:
                completeWebpage = urlWebpage + '&pagina=' + str(pageNumber)
                print completeWebpage

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkCells = baseSoup.findAll('div', { 'class' : 'prod_box' })[:-3]
                
                if len(ntbkCells) == 0:
                    break
                    
                print len(ntbkCells)                    
                for ntbkCell in ntbkCells:
                    print ntbkCell
                    link = ntbkCell.findAll('a')[1]
                    if link['href'] in pageLinks:
                        trigger = True
                        break
                    pageLinks.append(link)
                    
                    productData = ProductData()
                    productData.custom_name = link.string
                    productData.url = link['href']
                    productData.comparison_field = link['href']
                    
                    priceSpan = baseSoup.find('span', { 'class' : 'price' })
                    productData.price = int(priceSpan.string.replace('.', '').replace('$', ''))
                    print productData
                    productsData.append(productData)

                    
                pageNumber += 1
        return productsData

