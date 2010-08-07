#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class FullNotebook:
    name = 'FullNotebook'

    # Main method
    def getNotebooks(self):
        print 'Getting FullNotebook notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.fullnotebook.cl/'
        urlBuscarProductos = 'tienda/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'mini-notebooks/page/',
                    'notebooks/page/',
                    'netbook/page/',
                    ]
        
        for url_extension in url_extensions:
        
            # Primero necesitamos el numero de paginas
            firstUrl = urlBase + urlBuscarProductos + url_extension + '1'
            baseData = browser.open(firstUrl).get_data()
            baseSoup = BeautifulSoup(baseData)
            listaPags = baseSoup.find("span", {'class': 'pages'})
            last_page = int(listaPags.contents[0][-1])
            
            for i in range(last_page):
                pageUrl = urlBase + urlBuscarProductos + url_extension + str(i + 1)            

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(pageUrl).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                prices = []
                names = []
                urls = []
                
                rawLinks = baseSoup.findAll("div", { 'class':'cliente'})
                for rawLink in rawLinks:
                    names.append(rawLink.find("a").string)
                    urls.append(rawLink.find("a")['href'])
                    
                rawPrices = baseSoup.findAll("span", { 'id':'prei'})
                    
                for j in range(len(names)):
                    productData = ProductData()
                    productData.custom_name = names[j].encode('ascii','ignore').strip()
                    price = rawPrices[j].contents[0].replace("Precio:", '').replace('.', '').strip()
                    try:
                        productData.price = int(price)
                    except:
                        continue
                    productData.url = urls[j]
                    productData.comparison_field = productData.url
                    print productData
                    productsData.append(productData)

        return productsData

