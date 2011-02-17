#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Clie:
    name = 'Clie'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('td', { 'class': 'texto-neg-bold-ficha' }).string.split('&#8226;')[1].strip()
        product_price = int(product_soup.find('td', { 'background': 'images/ficha/bg_precio_normal_d.gif' }).find('a').string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Clie notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.clie.cl/'
        urlBuscarProductos = '?ver=4&categoria_producto='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  
                            '561',
                            '542',
                            '580',
                            '564',
                            '581',
                            '562',
                            '579',
                            '575',
                            '612',
                            '598',
                            '596',          
                            '595',
                            '178',
                            '500',
                            '158',
                            '307',                            
                            '308',
                            '646',  # Procesadores Intel     
                            ]
                            
        product_links = []
                            
        for url_extension in url_extensions:
            num_page = 1
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&pagina=' + str(num_page)
                print urlWebpage

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                productNameCells = baseSoup.findAll("td", { "colspan" : "2" })
                
                names = []
                prices = []
                
                if len(productNameCells) == 0:
                    break;
                    
                for productNameCell in productNameCells:
                    link = productNameCell.find('a')['onclick'].split('\'')[1]
                    product_links.append(urlBase + link)
                    
                num_page += 1
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            products_data.append(product)

        return products_data

