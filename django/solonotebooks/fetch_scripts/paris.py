#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup, ResultSet
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Paris(FetchStore):
    name = 'Paris'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h1', { 'class': 'txtDcsFch ubiDscFch' }).string.encode('ascii', 'ignore')
        
        product_prices = []
        
        try:
            product_price = int(product_soup.find('div', { 'class': 'txtPrecioPrin' }).find('b').contents[0].split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
        try:
            product_price = int(product_soup.find('div', { 'class': 'prcNrmlFc' }).find('b').string.split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
        try:
            product_price = int(product_soup.find('div', { 'class': 'prcIntFch2' }).find('b').string.split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
            
        if not product_prices:
            raise Exception
            
        product_price = min(product_prices)
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        browser = mechanize.Browser()
        
        urls = [
                    # Notebooks
                    ['http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51049202_18877035_si_2__18877035,50999203,51049192,51049202_', 'Notebook'],
                    # LCD
                    ['http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51056205_20096521_si_2__20096521,51056194,51056195,51056205_', 'Screen'],
                    ]
        
        product_links = []          
        for url, ptype in urls:

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
                
                product_links.append([link, ptype])

        return product_links
