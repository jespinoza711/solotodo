#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from utils import clean_price_string

class Paris(FetchStore):
    name = 'Paris'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        product_data = browser.open(product_link).get_data()
        soup = BeautifulSoup(product_data)

        name = soup.find('div', {'id': 'ficha-producto-nombre'})

        if not name:
            return None
        name = name.string.encode('ascii', 'ignore').strip()

        has_cencosud_card_price =\
        soup.find('div', {'id': 'ficha-producto-precio-mas'})

        if has_cencosud_card_price:
            mas_price = clean_price_string(has_cencosud_card_price.contents[0])
            price = int(mas_price)
        else:
            normal_price = soup.find('div', {'id': 'ficha-producto-precio'})
            normal_price = normal_price.string.split('$')[1]
            price = int(clean_price_string(normal_price))
        
        product_data = ProductData()
        product_data.custom_name = name
        product_data.price = price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        
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
