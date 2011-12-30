#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PortatilChile(FetchStore):
    name = 'PortatilChile'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('th', { 'colspan': '2' }).string.encode('ascii', 'ignore').split('"')[1]
        product_price = int(product_soup.find('table', { 'cellspacing': '1' }).find('table').findAll('td')[3].find('strong').string.replace('.', '').replace('&nbsp;', '').replace('$', '').strip())
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.portatilchile.cl/productos.html'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        baseData = browser.open(urlBase).get_data()
        baseSoup = BeautifulSoup(baseData)
        
        product_tables = baseSoup.findAll('table', { 'width': '226' })

        products_data = []

        for product_table in product_tables:
            link = product_table.find('a')['href']
            products_data.append([link, 'Notebook'])

        return products_data

