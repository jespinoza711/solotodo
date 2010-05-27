#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup, ResultSet
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Paris:
    name = 'Paris'

    # Main method
    def getNotebooks(self):
        print 'Getting Paris notebooks'
        # Basic data of the target webpage and the specific catalog
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        urls = ['http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51049202_18877035_si_2__18877035,50999203,51049192,51049202_'
                    ]
                            
        for url in urls:

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(url).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            mosaicDivs = baseSoup.findAll("div", { "class" : "cjPrdH2A" })
            
            otherDivs = baseSoup.findAll("div", { "class" : "cjPrdH2B" })
            
            for otherDiv in otherDivs:
                mosaicDivs.append(otherDiv)
            
            for mosaicDiv in mosaicDivs:
                productData = ProductData()
                
                divPrecioNormalConts1 = mosaicDiv.find("div", { "class" : "prcNrml2" })
                if not divPrecioNormalConts1:
                    break
                divPrecioNormalConts2 = divPrecioNormalConts1.find("a")                
                if divPrecioNormalConts2:
                    contents = divPrecioNormalConts2.contents[1].string.replace('&nbsp;', '').replace('Normal:', '').replace('Oferta:', '').replace('Normal:', '').replace('&#36;', '').replace('.', '').replace('$', '').strip()
                    precio = int(contents)
                    url1 = divPrecioNormalConts2['href']
                else:
                    
                    divPrecio1 = mosaicDiv.find("div", { "class" : "prcIntBll2" }).find("a")
                    contentsi = divPrecio1.contents[1].string
                    contentsi = contentsi.replace('$', '').replace('&nbsp;', '').replace('Oferta:', '').replace('Normal:', '').replace('&#36;', '').replace('.', '').strip()
                    precio = int(contentsi)
                    url1 = divPrecio1['href']
                    
                productData.price = precio
                
                divDesc = mosaicDiv.find("div", { "class" : "descP2" })
                name1 = divDesc.find("a").string
                linkId = int(divDesc.find('a')['id'].replace('prod', '')) + 1
                link = 'http://www.paris.cl/webapp/wcs/stores/servlet/productLP_10001_40000000577_-5_51049202_18877035_' + str(linkId) + '_18877035,50999203,51049192,51049202__listProd'
                
                productData.custom_name = name1.encode('ascii','ignore').strip()

                productData.url = link
                productData.comparison_field = productData.url
                
                print productData
                
                productsData.append(productData)

        return productsData

