#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PortatilChile:
    name = 'PortatilChile'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('th', { 'colspan': '2' }).string.encode('ascii', 'ignore').split('"')[1]
        product_price = int(product_soup.find('table', { 'cellspacing': '1' }).find('table').findAll('td')[5].find('strong').string.replace('.', '').replace('&nbsp;', '').replace('$', '').strip())
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting PortatilChile notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.portatilchile.cl/modules/rmms/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        baseData = browser.open(urlBase).get_data()
        baseSoup = BeautifulSoup(baseData)
        
        productTable = baseSoup.find('table', { 'class': 'outer' })
        productRows = productTable.findAll('tr', recursive = False)
        productCells = []
        product_links = []
        for productRow in productRows:
            productCells.extend(productRow.findAll('td', recursive = False))
        
        # Array containing the data for each product
        products_data = []
        
        for productCell in productCells:
            link = urlBase + productCell.find('a')['href']
            product_links.append(link)

        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

