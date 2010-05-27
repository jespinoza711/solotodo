#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class NotebookCenter:
    name = 'NotebookCenter'

    # Main method
    def getNotebooks(self):
        print 'Getting NotebookCenter notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.notebookcenter.cl/'
        urlBuscarProductos = 'listado_productos_NEW.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?id_categoria=401',
                            '?id_categoria=402',
                            '?id_categoria=403',
                            '?id_categoria=404',
                            '?id_categoria=405',
                            '?id_categoria=406',
                            '?id_categoria=407',
                            '?id_categoria=429',
                            '?id_categoria=440',
                            '?id_categoria=61',
                            '?id_categoria=256',
                            '?id_categoria=251',
                            '?id_categoria=57',
                            '?id_categoria=64',
                            '?id_categoria=58',
                            '?id_categoria=418',
                            '?id_categoria=212',
                            '?id_categoria=63',
                            '?id_categoria=232',
                            '?id_categoria=308',
                            '?id_categoria=307',
                            '?id_categoria=437',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            
            prices = []
            names = []
            urls = []

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawNames = baseSoup.findAll("span", { "class" : "subtit2" })
            
            for rawName in rawNames:
                subNames = rawName.contents
                name = '';
                for subName in subNames:
                    try:
                        name = (name + ' ' + subName.strip()).strip()
                    except:
                        continue
                names.append(name)
                
            rawLinks = baseSoup.findAll("td", { "height" : "120" })
            
            for rawLink in rawLinks:
                urls.append(urlBase + rawLink.find("a")['href'])
                
            rawPrices = baseSoup.findAll("span", { "class" : "precionormal" })
            
            for rawPrice in rawPrices:
                price = rawPrice.contents[0].replace('$', '').replace('.', '').replace('&nbsp;', '')
                prices.append(int(price))
                
            for i in range(len(names)):
                productData = ProductData()
                productData.custom_name = names[i].encode('ascii','ignore').strip()
                productData.price = prices[i]
                productData.url = urls[i]
                productData.comparison_field = productData.url
                print productData
                productsData.append(productData)

        return productsData

