#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup, ResultSet
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Paris(FetchStore):
    name = 'Paris'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link, already_tried=False):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except Exception:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried=True)

        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'id': 'ficha-producto-nombre' }).string.encode('ascii', 'ignore').strip()
                
        product_prices = []
        
        try:
            product_price = int(product_soup.find('div', { 'id': 'ficha-producto-precio' }).string.split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
            
        try:
            product_price = int(product_soup.find('div', { 'id': 'ficha-producto-precio-normal' }).string.split('$')[1].replace('.', ''))
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
                    ['http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51145648_18877035_si_2__18877035,50999203,51145648_', 'Notebook'],
                    # Netbooks
                    ['http://www.paris.cl/webapp/wcs/stores/servlet/category_10001_40000000577_-5_51056269_18877035_51039699_18877035,51039699,51056269', 'Notebook'],
                    # LCD
                    ['http://www.paris.cl/webapp/wcs/stores/servlet/categoryTodos_10001_40000000577_-5_51056211_20096521_si_2__20096521,51056194,51056196,51056211_', 'Screen'],
                    ]
        
        product_links = []          
        for url, ptype in urls:
            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(url).get_data()
            baseData = unicode(baseData, errors='ignore')
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            link_divs = baseSoup.findAll("div", { "class" : "descP2011" })
            
            for div in link_divs:
                linkId = int(div.find('a')['id'].replace('prod', '')) + 1

                link = 'http://www.paris.cl/webapp/wcs/stores/servlet/productLP_10001_40000000577_-5_51049202_18877035_' + str(linkId) + '_18877035,50999203,51049192,51049202__listProd'
                
                product_links.append([link, ptype])
                

        return product_links
