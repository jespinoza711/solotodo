#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PackardBell(FetchStore):
    name = 'Packard Bell'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        try:
            avail = int(product_soup.find('span', { 'class': 'unidades' }).string)
            if not avail:
                return None
        except:
            return None
        
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
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.packardbell.cl'
        urlCatalog = '/2010/catalogo/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
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
                
        return product_links

