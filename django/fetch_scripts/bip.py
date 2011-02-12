#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bip:
    name = 'Bip'

    # Method that extracts the <a> tags to products given the URL of the catalog page
    def extract_links(self, pageUrl):
        br = mechanize.Browser()
        data = br.open(pageUrl).get_data()
        soup = BeautifulSoup(data)
        links = soup.findAll("a", { "class" : "menuprod" })[::2]

        return links

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()
        
        stock_info = soup.find('td', { 'class' : 'disp' }).contents
        stock_string = ''.join(str(stock) for stock in stock_info)
        
        if 'Agotado' in stock_string:
            return None

        titleSpan = soup.find("td", { "class" : "menuprodg" })
        title = titleSpan.string.strip()

        priceCell = soup.findAll("td", { "class" : "prc8" })
        price = int(str(priceCell[1].string).replace('.', '').replace('$', '').strip())

        productData.custom_name = title.encode('ascii','ignore').strip()
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url	    

        print productData
        return productData

    # Main method
    def get_products(self):
        print 'Getting Bip notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.bip.cl/ecommerce/'
        urlBuscarProductos = 'index.php?modulo=busca&'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'categoria=191',                    # Netbooks
                            'categoria=166',                    # Notebooks
                            'categoria=118&categoria_papa=97',  # Tarjetas de video
                            ]
                            
        productLinks = []
                            
        for url_extension in url_extensions:
            page_number = 0
            
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&pagina=' + str(page_number)
                
                rawLinks = self.extract_links(urlWebpage)
                if not rawLinks:
                    break
                for rawLink in rawLinks:
                    productLinks.append(urlBase + rawLink['href'])
                
                page_number += 1
        
                
        for productLink in productLinks:
            prod = self.retrieve_product_data(productLink)
            if prod:
                productsData.append(prod)
        
        return productsData

