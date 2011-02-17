#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bym:
    name = 'Bym'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        base_data = browser.open(product_link).get_data()
        base_soup = BeautifulSoup(base_data)
        
        product_data = ProductData()
        
        stock_image_url = base_soup.findAll('div', { 'class' : 'textOtrosPrecios' })[2].find('img')['src']
        if 'agotado' in stock_image_url:
            return None
        
        title = base_soup.find('div', { 'class' : 'textTituloProducto'}).string.strip()
        
        prices = base_soup.findAll('div', { 'class' : 'textOtrosPrecios' })
        price = prices[0].string
        price = int(price.replace('.', '').replace('$', ''))

        product_data.custom_name = title
        product_data.price = price
        product_data.url = product_link.split('&osCsid')[0]
        product_data.comparison_field = product_data.url	 
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Bym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ttchile.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  
                            'subpro.php?idCat=21&idSubCat=20',  # Notebooks
                            'catpro.php?idCat=31',              # Tarjetas de video
                            'catpro.php?idCat=25',              # Procesadores AMD
                            'catpro.php?idCat=26',              # Procesadores Intel
                            ]
                            
        for url_extension in url_extensions:
            page_number = 1
            
            while True:
                urlWebpage = urlBase + url_extension + '&pagina=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                base_data = browser.open(urlWebpage).get_data()
                base_soup = BeautifulSoup(base_data)
                
                productLinks = [div.find('a')['href'] for div in base_soup.findAll('div', {'class': 'linkTitPro'})]
                
                if not productLinks:
                    break
                
                for productLink in productLinks:
                    product_link = urlBase + productLink
                    
                    product = self.retrieve_product_data(product_link)
                    if product:
                        products_data.append(product)
                
                page_number += 1

        return products_data

