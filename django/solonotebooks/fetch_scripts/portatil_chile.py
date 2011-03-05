#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PortatilChile:
    name = 'PortatilChile'
    use_existing_links = False
    
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
        
        return product_data

    # Main method
    def retrieve_product_links(self):
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

        return product_links

