#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Clie:
    name = 'Clie'

    # Main method
    def getNotebooks(self):
        print 'Getting Clie notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.clie.cl/'
        urlBuscarProductos = '?ver=4&categoria_producto='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '561',
                            '542',
                            '580',
                            '564',
                            '581',
                            '562',
                            '579',
                            '575',
                            '576',
                            '612',
                            '598',                                                        
                            '243',                            
                            '596',                                                        
                            '595',                                                        
                            '178',
                            '500',
                            '158',
                            '307',
                            '308',                            
                            ]
                            
        for url_extension in url_extensions:
            num_page = 1
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&pagina=' + str(num_page)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                productNameCells = baseSoup.findAll("td", { "colspan" : "2" })
                
                names = []
                prices = []
                onclicks = []
                
                if len(productNameCells) == 0:
                    break;
                    
                for productNameCell in productNameCells:
                    name = productNameCell.find("a").string.strip()
                    onclick = productNameCell.find('a')['onclick'].split('\'')[1]
                    names.append(name)
                    onclicks.append(onclick)
                    
                productPriceCells = baseSoup.findAll("td", { "background" : "images/ficha/bg_precio_normal_d.gif" })
                
                for productPriceCell in productPriceCells:
                    priceString = productPriceCell.findAll("a")[1].string.replace('.', '').strip()
                    price = int(priceString)
                    prices.append(price)
                    
                for i in range(len(names)):
                    productData = ProductData()
                    productData.custom_name = names[i].encode('ascii','ignore').strip()
                    productData.price = prices[i]
                    productData.url = urlBase + onclicks[i]
                    productData.comparison_field = productData.url
                    print productData
                    productsData.append(productData)
                    
                num_page += 1

        return productsData

