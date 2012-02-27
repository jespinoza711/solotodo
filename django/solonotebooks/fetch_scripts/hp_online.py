#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class HPOnline(FetchStore):
    name = 'HP Online'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        # Double open URL because the first redirects to home and sets a cookie
        BeautifulSoup(browser.open(product_link).get_data())
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        product_name = product_soup.findAll('h2')[-1].string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('h1', { 'class': 'bigtitle' }).contents[0].split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.hponline.cl'
        urlBuscarProductos = '/personas/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['categoria.aspx?cat=ZA==&V=G', 'Notebook'],
                            ]
                          
        product_links = []                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            ntbkCells = baseSoup.findAll('div', { 'class' : 'product' })
            
            for ntbkCell in ntbkCells:
                product_links.append([urlBase + ntbkCell.find('a')['href'], ptype])
                
        return product_links
