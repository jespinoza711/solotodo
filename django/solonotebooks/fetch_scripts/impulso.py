#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class Impulso:
    name = 'Impulso'

    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_title = product_soup.find('h2').string
        product_price = int(product_soup.find('span', { 'id': 'our_price_display'}).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_title
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        print product_data
        
        return product_data

    def get_products(self):
        print 'Getting Impulso notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://impulso.cl'
        urlBuscarProductos = '/prestashop/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        product_links = []
        
        url_extensions = [  
                            '32-notebooks',
                            '35-netbooks',
                            '37-tablets',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            prod_list = baseSoup.find('ul', {'id': 'product_list'})
            
            if not prod_list:
                continue
            
            prod_cells = prod_list.findAll('li')

            for cell in prod_cells:
                product_links.append(cell.find('a')['href'])
                
            
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                productsData.append(product)
                
        return productsData

