#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Sym(FetchStore):
    name = 'Sym'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)
        
        stock_status = soup.find('li', { 'class' : 'stocks' }).findAll('span')[1].contents[0]
        
        if 'pedido' not in stock_status and 'stock' not in stock_status:
            return None

        productData = ProductData()

        titleSpan = soup.find("h1")
        title = str(titleSpan.string).strip()
        
        price = int(soup.find('span', { 'class': 'red' }).find('strong').string.replace('$', '').replace('.', ''))

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.sym.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        
        url_extensions = [
            ['?cat=104', 'Notebook'],       # Notebooks
            ['?cat=32_68', 'VideoCard'],    # Tarjetas de video AGP
            ['?cat=32_69', 'VideoCard'],    # Tarjetas de video PCIe
            ['?cat=50', 'Processor'],       # Procesadores Intel
            ['?cat=25', 'Processor'],       # Procesadores AMD
            ['?cat=81', 'Screen'],          # Monitores LCD
            ['?cat=26', 'Motherboard'],     # MB AMD
            ['?cat=49', 'Motherboard'],     # MB Intel
            ['?cat=27', 'Ram'],             # RAM
        ]
                            
        productLinks = []
        links = []
                            
        for url_extension, ptype in url_extensions:
            page_number = 1
            
            while True:
                urlWebpage = urlBase + url_extension + '&page=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                rawLinks = baseSoup.findAll("div", { "class" : "listadoindiv" })
                
                if not rawLinks:
                    break
                
                break_flag = False
                
                for rawLink in rawLinks:
                    link = rawLink.find("h2").find("a")['href']
                    if link in links:
                        break_flag = True
                        break 
                    links.append(link)
                    productLinks.append([link, ptype])
                    
                if break_flag:
                    break
                    
                page_number += 1

        return productLinks

