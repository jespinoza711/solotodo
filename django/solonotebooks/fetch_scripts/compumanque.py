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
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        title = soup.find('h1').string
        price = int(soup.findAll('b')[1].parent.parent.findAll('td')[1].string.replace('$', '').replace('.', ''))
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData


    def retrieve_product_links(self):
        urlBase = 'http://72.249.5.151/~compucl/index.php?route=product/category&path='
        browser = mechanize.Browser()
        
        url_extensions = [  '101_87',    # Tarjetas de video
                            '19',     # Procesadores
                            '45_97',    # Monitores
                            '45_98',    # TV
                            '106',   # Netbooks
                            '50',     # Notebooks
                            ]
                            
        product_links = []
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData).find('table', { 'class' : 'list' })
            
            if not baseSoup:
                continue

            rawLinks = baseSoup.findAll('a')[::2]
            
            for rawLink in rawLinks:
                link = rawLink['href']
                product_links.append(link)
                    
        return product_links

