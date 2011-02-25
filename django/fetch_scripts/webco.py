#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Webco:
    name = 'Webco'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h1').contents[0].encode('ascii', 'ignore')
        product_price = int(product_soup.find('h2').find('a').string.replace('.', '').replace('$', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Webco notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www1.webco.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  # Netbooks
                            'n_new_productos.asp?CATEGORIA={761FD739-2D0F-4177-8AE0-C641D6F16502}',
                            # Notebooks
                            'n_new_productos.asp?CATEGORIA={D70BBB30-F5E9-4246-B812-A939C8777429}',
                            # Tarjetas de video
                            'n_new_productos.asp?CATEGORIA={FFE74755-6E24-4958-A066-F75670943D3E}',
                            # Procesadores AMD
                            'n_new_productos.asp?CATEGORIA={AA5D5535-B127-4AEE-8583-4529F66DE4D7}#ct_39',
                            # Procesadores Intel
                            'n_new_productos.asp?CATEGORIA={5701C20F-03E6-430E-8CCF-01EE820BEDF8}#ct_39',
                            # LCD TV
                            'n_new_productos.asp?CATEGORIA={E49A199E-214A-4658-99AA-7E6220434D8D}#ct_32',
                            # LCD
                            'n_new_productos.asp?CATEGORIA={79A1AF72-4B4D-4368-9205-FC0D646A1145}#ct_32',
                            ]
        
        product_links = []                    
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            print urlWebpage

            productImages = baseSoup.findAll("img", { "width" : "193" })
            
            for productImage in productImages:
                productData = ProductData()
                try:
                    product_links.append(urlBase + productImage.parent['href'])
                except:
                    continue
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data


