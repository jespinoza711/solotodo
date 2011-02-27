#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Racle:
    name = 'Racle'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        try:
            product_name = product_soup.findAll('h1')[1].string.encode('ascii', 'ignore').strip()
        except:
            return None
        product_price = int(product_soup.find('span', { 'class': 'productPrice' }).string.replace('.', '').replace('$', '').replace(' ', '').strip())
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data
    
    # Main method
    def get_products(self):
        print 'Getting Racle notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.racle.cl'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        urlSearch = '/ventas/'            

        urlExtensions = [
                            'tienda/netbook', 
                            'tienda/notebook',
                            'tienda/monitor',
                            'tieda/moitor-led',
                        ]
        product_links = []
        for urlExtension in urlExtensions:
            urlWebpage = urlBase + urlSearch + urlExtension + '?limit=50&limitstart=0'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productDetailsCells = baseSoup.findAll('td', { 'class' : 'producto_fondo_tabla_M' })
            
            for productDetailCell in productDetailsCells:
                productLink = productDetailCell.find('a', { 'class' : 'producto_titulo' })
                product_links.append(urlBase + productLink['href'].split('?')[0])
            
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

