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

        title = soup.findAll('b')[2].string.encode('ascii', 'ignore')
        
        price = int(soup.find('font', {'size':'3'}).find('span').find('span').find('b').string.replace('$', '').replace(',', ''))

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
            ['75_136', 'Notebook'],   # Notebooks
            ['83_157', 'VideoCard'],   # Tarjetas de video AGP
            ['83_158', 'VideoCard'],   # Tarjetas de video PCIe AMD
            ['83_159', 'VideoCard'],   # Tarjetas de video PCIe Nvidia
            ['61_85', 'Processor'],    # Procesadores AM2
            ['61_84', 'Processor'],    # Procesadores AM3
            ['61_86', 'Processor'],    # Procesadores 775
            ['61_193', 'Processor'],   # Procesadores 1155
            ['61_87', 'Processor'],    # Procesadores 1156
            ['61_165', 'Processor'],   # Procesadores 1366
            ['73_128', 'Screen'],   # LCD
            ['73_129', 'Screen'],   # LCD/TV
            ['73_171', 'Screen'],   # LED
            ['60_88', 'Motherboard'],   # Placas madre AM2
            ['60_89', 'Motherboard'],   # Placas madre AM3
            ['60_90', 'Motherboard'],   # Placas madre 775
            ['60_194', 'Motherboard'],   # Placas madre 1155
            ['60_91', 'Motherboard'],   # Placas madre 1156
            ['60_186', 'Motherboard'],   # Placas madre 1366
            ['72_126', 'Ram'],   # RAM Desktop
            ['72_127', 'Ram'],   # RAM Notebook
            ['62_101', 'StorageDrive'],   # HDD PC
            ['62_103', 'StorageDrive'],   # HDD Notebook
            ['70_118', 'PowerSupply'],   # Fuentes de poder
        ]
                            
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            td_products = baseSoup.findAll('td', { 'class' : 'wrapper_pic_br wrapper_pic_td' })
            
            
            for td_product in td_products:
                link = td_product.find('a')['href']
                product_links.append([link, ptype])
                    
        return product_links

