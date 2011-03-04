#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Bym(FetchStore):
    name = 'Bym'
    use_existing_links = True
    
    def retrieve_product_data(self, product_link, already_tried = False):
        browser = mechanize.Browser()
        try:
            base_data = browser.open(product_link).get_data()
        except:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)
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
        
        return product_data

    def retrieve_product_links(self):
        urlBase = 'http://www.ttchile.cl/'        
        browser = mechanize.Browser()
        product_links = []
        
        url_extensions = [  
                            'subpro.php?idCat=21&idSubCat=20',  # Notebooks
                            'catpro.php?idCat=31',              # Tarjetas de video
                            'catpro.php?idCat=25',              # Procesadores AMD
                            'catpro.php?idCat=26',              # Procesadores Intel
                            'catpro.php?idCat=18',              # LCD
                            ]
                            
        for url_extension in url_extensions:
            page_number = 1
            
            while True:
                urlWebpage = urlBase + url_extension + '&pagina=' + str(page_number)
                base_data = browser.open(urlWebpage).get_data()
                base_soup = BeautifulSoup(base_data)
                
                productLinks = [div.find('a')['href'] for div in base_soup.findAll('div', {'class': 'linkTitPro'})]
                
                if not productLinks:
                    break
                
                for productLink in productLinks:
                    product_links.append(urlBase + productLink)
                
                page_number += 1

        return product_links

