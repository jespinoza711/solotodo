#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PCExpress(FetchStore):
    name = 'PC Express'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, product_link):
        br = mechanize.Browser()
        data = br.open(product_link).get_data()
        soup = BeautifulSoup(data)
        productData = ProductData()

        title = soup.findAll('b')[2].string
        
        price = int(soup.find('font', {'size':'3'}).find('span').contents[1].string.replace('$', '').replace(',', ''))

        productData.custom_name = title
        productData.price = price
        productData.url = product_link
        productData.comparison_field = product_link
        return productData


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pc-express.cl/index.php?cPath='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  
                            '75_136',   # Notebooks
                            '83_157',   # Tarjetas de video AGP
                            '83_158',   # Tarjetas de video PCIe AMD
                            '83_159',   # Tarjetas de video PCIe Nvidia
                            '61_85',    # Procesadores AM2
                            '61_84',    # Procesadores AM3
                            '61_86',    # Procesadores 775
                            '61_193',   # Procesadores 1155
                            '61_87',    # Procesadores 1156
                            '61_165',   # Procesadores 1366
                            '73_128',   # LCD
                            '73_129',   # LCD/TV
                            '73_171',   # LED
                        ]
                            
        product_links = []
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            td_products = baseSoup.findAll('td', { 'class' : 'wrapper_pic_br wrapper_pic_td' })
            
            
            for td_product in td_products:
                link = td_product.find('a')['href']
                product_links.append(link)
                    
        return product_links

