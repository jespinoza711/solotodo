#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class PackardBell:
    name = 'Packard Bell'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'class': 'tit_prod_det' }).string.encode('ascii', 'ignore').strip()
        try:
            product_price = int(product_soup.find('div', { 'class': 'precio_det' }).contents[0].replace('.', ''))
        except:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting Packard Bell notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.packardbell.cl'
        urlCatalog = '/2010/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  '116-Netbook.html',
                            '112-Notebook.html',
                            ]
                            
        product_links = []          
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlCatalog + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            imgTags = baseSoup.findAll('div', { 'class' : 'img_prod' })            
            
            for i in range(len(imgTags)):
                link = imgTags[i]['onclick'].replace('javascript:location.href=\'', '').replace('\'', '')
                product_links.append(link)
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

