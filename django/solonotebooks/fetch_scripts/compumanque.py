#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Compumanque(FetchStore):
    name = 'Compumanque'
    use_existing_links = False

    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        try:
            data = br.open(productUrl).get_data()
        except:
            return None
        soup = BeautifulSoup(data)

        try:
            title = soup.find('h1').string
            price = int(soup.findAll('b')[1].parent.parent.findAll('td')[1].string.replace('$', '').replace('.', ''))
        except:
            return None
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData


    def retrieve_product_links(self):
        urlBase = 'http://72.249.5.151/~compucl/index.php?route=product/category&path='
        browser = mechanize.Browser()
        
        url_extensions = [
            ['101_87', 'VideoCard'],    # Tarjetas de video
            ['19', 'Processor'],     # Procesadores
            ['45_97', 'Screen'],    # Monitores
            ['45_98', 'Screen'],    # TV
            ['106', 'Notebook'],   # Netbooks
            ['50', 'Notebook'],     # Notebooks
            ['79', 'Motherboard'],      # Placas madre
            ['122_121', 'Ram'],      # Ram Notebook
            ['122_57', 'Ram'],      # Ram PC
        ]
                            
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData).find('table', { 'class' : 'list' })
            
            if not baseSoup:
                continue

            rawLinks = baseSoup.findAll('a')[::2]
            
            for rawLink in rawLinks:
                link = rawLink['href']
                product_links.append([link, ptype])
                    
        return product_links

