#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class Sym:
    name = 'Sym'

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
        
        price = int(soup.find('div', { 'id': 'product-info' }).find('ul').findAll('li')[-1].contents[1].replace('$', '').replace('.', ''))

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        print productData
        return productData


    # Main method
    def get_products(self):
        print 'Getting Sym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.sym.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  '?cat=104',         # Notebooks
                            '?cat=32_68',       # Tarjetas de video AGP
                            '?cat=32_69',       # Tarjetas de video PCIe
                            '?cat=50',          # Procesadores Intel
                            '?cat=25',          # Procesadores AMD
                            '?cat=81',          # Monitores LCD
                            ]
                            
        productLinks = []
                            
        for url_extension in url_extensions:
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
                    if link in productLinks:
                        break_flag = True
                        break 
                    productLinks.append(link)
                    
                if break_flag:
                    break
                    
                page_number += 1
                    
        for productLink in productLinks:
            prod = self.retrieve_product_data(productLink)
            if prod:
                productsData.append(prod)
                    

        return productsData

