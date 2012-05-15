#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Rigam(FetchStore):
    name = 'Rigam'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        availability = product_soup.find('b', { 'style': 'color:red;' })
        if availability:
            if 'PRODUCTO AGOTADO' in availability.string:
                return None
        
        product_name = product_soup.find('td', { 'class': 'cy2' }).find('strong').contents[0].encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'class': 'cy3' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.rigam.cl/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [
            ['index.php?act=viewCat&catId=39', 'Notebook'],   # Notebooks
            ['index.php?act=viewCat&catId=60', 'VideoCard'],    # Tarjetas de video
            ['index.php?act=viewCat&catId=40', 'Processor'],   # Procesadores AMD
            ['index.php?act=viewCat&catId=2', 'Processor'],     # Procesadores Intel
            ['index.php?act=viewCat&catId=54', 'Screen'],    # Monitores
            ['index.php?act=viewCat&catId=3', 'Motherboard'], # MB AMD
            ['index.php?act=viewCat&catId=52', 'Motherboard'], # MB Intel
            ['index.php?act=viewCat&catId=35', 'Ram'], # RAM
            ['index.php?act=viewCat&catId=70', 'StorageDrive'], # HDD Notebook
            ['index.php?act=viewCat&catId=58', 'StorageDrive'], # HDD SATA
            ['index.php?act=viewCat&catId=59', 'PowerSupply'], # Fuentes de poder
            ['index.php?act=viewCat&catId=32', 'ComputerCase'], # Gabinetes
        ]
        
        product_links = []                    
        for url_extension, ptype in url_extensions:
            page_number = 0
            
            while True:
                urlWebpage = urlBase + url_extension + '&page=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                products_table = baseSoup.find('table', { 'class' : 'tblList' })
                
                if not products_table:
                    break
                
                product_rows = products_table.findAll('tr')[1:]
                
                for product_row in product_rows:
                    link = product_row.find('a', { 'class' : 'txtDefault' })
                    product_links.append([urlBase + link['href'], ptype])
                    
                page_number += 1

        return product_links

