#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class NotebookCenter:
    name = 'NotebookCenter'

    # Main method
    def get_products(self):
        print 'Getting NotebookCenter notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.notebookcenter.cl/'
        urlBuscarProductos = 'centrodetalle.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?id_categoria=308', # Macbook Air
                            '?id_categoria=307', # Macbook Pro
                            '?id_categoria=403', # Netbook HP
                            '?id_categoria=404', # Netbook Lenovo
                            '?id_categoria=405', # Netbook Packard Bell
                            '?id_categoria=406', # Netbook Samsung
                            '?id_categoria=429', # Netbook Sony
                            '?id_categoria=440', # Netbook Viewsonic
                            '?id_categoria=61',  # Notebook Acer
                            '?id_categoria=251', # Notebook Dell
                            '?id_categoria=505', # Notebook Gamer
                            '?id_categoria=57',  # Notebook HP
                            '?id_categoria=64',  # Notebook Lenovo
                            '?id_categoria=342', # Notebook MSI
                            '?id_categoria=58',  # Notebook Packard Bell
                            '?id_categoria=418', # Notebook Samsung
                            '?id_categoria=212', # Notebook Sony
                            '?id_categoria=63',  # Notebook Toshiba
                            '?id_categoria=534', # Notebook Viewsonic
                            ]
                            
        for url_extension in url_extensions:
            index = 1
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&indice=' + str(index)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                prices = []
                names = []
                urls = []

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                rawNames = baseSoup.findAll("span", { "class" : "subtit2" })[1::2]
                
                if not rawNames:
                    break
                
                
                for rawName in rawNames:
                    subNames = [str(subName) for subName in rawName.contents]
                    name = ''.join(subNames).strip()
                    names.append(name)
                    
                rawLinks = baseSoup.findAll("a", { "target" : "ifrm_centro" })
                
                for rawLink in rawLinks:
                    link = urlBase + rawLink['href']
                    link = link.split('&id_categoria')[0]
                    urls.append(link)
                    
                rawPrices = baseSoup.findAll("span", { "class" : "precionormal" })
                
                for rawPrice in rawPrices:
                    price = rawPrice.contents[0].replace('$', '').replace('.', '').replace('&nbsp;', '')
                    prices.append(int(price))
                    
                for i in range(len(names)):
                    productData = ProductData()
                    productData.custom_name = unicode(names[i], errors  = 'ignore').strip()
                    productData.price = prices[i]
                    productData.url = urls[i]
                    productData.comparison_field = productData.url
                    print productData
                    productsData.append(productData)
                    
                index += 1

        return productsData

