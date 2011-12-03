#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from django.utils.http import urlquote

class Bym(FetchStore):
    name = 'Bym'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link, already_tried = False):
        new_product_link = 'http://www.dcc.uchile.cl/~vkhemlan/index.php?url=' + urlquote(product_link)
        try:
            base_data = mechanize.urlopen(new_product_link)
        except Exception:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)
        base_soup = BeautifulSoup(base_data)
        
        product_data = ProductData()
        
        stock_image_url = base_soup.findAll('div', { 'class' : 'textOtrosPrecios' })[2].find('img')['src']
        if 'agotado' in stock_image_url:
            return None
        
        title = base_soup.find('div', { 'class' : 'textTituloProducto'}).string.strip().encode('ascii', 'ignore')
        
        prices = base_soup.findAll('div', { 'class' : 'textPrecioContado' })
        price = prices[0].string
        price = int(price.replace('.', '').replace('$', ''))

        product_data.custom_name = title
        product_data.price = price
        product_data.url = product_link.split('&osCsid')[0]
        product_data.comparison_field = product_data.url	 
        
        return product_data

    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        urlBase = 'http://www.ttchile.cl/'        
        product_links = []
        
        url_extensions = [  
                            ['catpro.php?ic=21&isc=20', 'Notebook'],  # Notebooks
                            ['catpro.php?ic=31', 'VideoCard'],              # Tarjetas de video
                            ['catpro.php?ic=25', 'Processor'],             # Procesadores AMD
                            ['catpro.php?ic=26', 'Processor'],             # Procesadores Intel
                            ['catpro.php?ic=18', 'Screen'],             # LCD
                            ['catpro.php?ic=23', 'Motherboard'],             # MB AMD
                            ['catpro.php?ic=24', 'Motherboard'],             # MB Intel
                            ]
                            
        for url_extension, ptype in url_extensions:
            page_number = 1
            
            while True:
                initial_url = urlBase + url_extension + '&pagina=' + str(page_number)
                urlWebpage = 'http://www.dcc.uchile.cl/~vkhemlan/index.php?url=' + urlquote(initial_url)
                base_data = mechanize.urlopen(urlWebpage)
                base_soup = BeautifulSoup(base_data)
                
                productLinks = [div.find('a')['href'] for div in base_soup.findAll('div', {'class': 'linkTitPro'})]
                
                if not productLinks:
                    break
                
                for productLink in productLinks:
                    url = urlBase + productLink
                    product_links.append([url, ptype])
                
                page_number += 1

        return product_links

