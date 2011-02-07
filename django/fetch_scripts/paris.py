#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup, ResultSet
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Paris:
    name = 'Paris'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h1', { 'class': 'txtDcsFch ubiDscFch' }).string.encode('ascii', 'ignore')
        
        product_price = None
        try:
            product_price = int(product_soup.find('div', { 'class': 'prcNrmlFc' }).find('b').string.split('$')[1].replace('.', ''))
        except:
            pass
            
        if not product_price:
            try:
                product_price = int(product_soup.find('div', { 'class': 'prcIntFch2' }).find('b').string.split('$')[1].replace('.', ''))
            except:
                pass
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def getNotebooks(self):
        print 'Getting Paris notebooks'
        # Basic data of the target webpage and the specific catalog
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        urls = [
                    'http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51049202_18877035_si_2__18877035,50999203,51049192,51049202_'
                    ]
        
        product_links = []          
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
                
                divDesc = mosaicDiv.find("div", { "class" : "descP2" })
                linkId = int(divDesc.find('a')['id'].replace('prod', '')) + 1
                link = 'http://www.paris.cl/webapp/wcs/stores/servlet/productLP_10001_40000000577_-5_51049202_18877035_' + str(linkId) + '_18877035,50999203,51049192,51049202__listProd'
                
                product_links.append(link)

        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data
