#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Clie(FetchStore):
    name = 'Clie'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        availability_text = product_soup.findAll('td', { 'class': 'texto-neg-bold' })[-1].find('a').string.strip()
        if availability_text[0] == '0':
            return None
        
        product_name = product_soup.find('td', { 'class': 'tit-nar-bold' }).contents[0].split('&#8226;')[0].replace('&nbsp;&raquo; ', '').strip()
        product_price = int(product_soup.find('td', { 'background': 'images/ficha/bg_efectivo_d.gif' }).find('a').string.replace('$', '').replace('.', ''))
        
        if not product_price:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        url_base = 'http://www.clie.cl/'
        browser = mechanize.Browser()

        category_codes = [
            ['157', 'Notebook'],        # Notebooks
            ['433', 'StorageDrive'],    # PC HDDs
            ['275', 'StorageDrive'],    # Notebook HDDs
            ['25', 'Ram'],              # PC Ram
            ['25', 'Ram'],              # PC Ram
            ['392', 'Ram'],             # Notebook Ram
            ['615', 'Monitor'],         # LED Monitor
            ['18', 'Monitor'],          # LCD Monitor
            ['265', 'Television'],      # LCD Television
            ['613', 'Television'],      # LED Television
            ['645', 'Processor'],       # Processors
            ['759', 'ComputerCase'],    # Computer cases
        ]

        product_links = []

        product_pages_urls = []

        for code, ptype in category_codes:
            category_url = 'http://www.clie.cl/?categoria=' + code
            soup = BeautifulSoup(browser.open(category_url).get_data())

            brands_table = soup.find('table', {'width': '150'})
            brand_links = brands_table.findAll('a', {'id': 'ocultar'})

            for link in brand_links:
                complete_url = 'http://www.clie.cl/' + link['href']
                product_pages_urls.append([complete_url, ptype])

        manual_brand_urls = [
            # HP Netbooks
            ['http://www.clie.cl/?categoria_producto=561&categoria=&ver=4',
             'Notebook'],
            # Toshiba Netbooks
            ['http://www.clie.cl/?categoria_producto=564&categoria=&ver=4',
             'Notebook'],
            # Acer Netbooks
            ['http://www.clie.cl/?categoria_producto=562&categoria=&ver=4',
             'Notebook'],
            # Lenovo Netbooks
            ['http://www.clie.cl/?categoria_producto=579&categoria=&ver=4',
             'Notebook'],
            # Apple Macbook Air
            ['http://www.clie.cl/?categoria_producto=726&categoria=0&ver=4',
             'Notebook'],
            # Apple Macbook Pro
            ['http://www.clie.cl/?categoria_producto=725&categoria=0&ver=4',
             'Notebook'],
            ]

        product_pages_urls.extend(manual_brand_urls)

        for page_url, ptype in product_pages_urls:
            num_page = 1
            while True:
                url_webpage = page_url + '&pagina=' + str(num_page)

                soup = BeautifulSoup(browser.open(url_webpage).get_data())
                product_cells = soup.findAll('td', {'colspan': '2'})[1:]

                if not product_cells:
                    break

                for product_cell in product_cells:
                    link = product_cell.find('a')
                    url = link['onclick'].split('\'')[1]
                    product_links.append([url_base + url, ptype])

                num_page += 1

        return product_links
