#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class RkNotebooks(FetchStore):
    name = 'rK-Notebooks'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h2').string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'id': 'our_price_display' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.rk-notebooks.cl/store/category.php?id_category='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [
                           '7',
                            ]
        
        product_links = []                
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            titles = baseSoup.findAll('h3')

            for i in range(len(titles)):
                product_links.append(titles[i].find('a')['href'])

        return product_links

