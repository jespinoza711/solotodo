#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

class MacOnline(FetchStore):
    name = 'MacOnline'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        soup = BeautifulSoup(product_data)

        name = soup.findAll('h2')[1]
        name = name.string.strip().encode('ascii', 'ignore')

        price = soup.find('span', {'itemprop': 'price'}).contents[0]
        price = int(clean_price_string(price))

        product_data = ProductData()
        product_data.custom_name = name
        product_data.price = price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        url_base = 'http://www.maconline.cl'
        browser = mechanize.Browser()
        product_links = []

        url_extensions = [
            ['397.html', 'Notebook'],
            ['421.html', 'Notebook'],
            ['513.html', 'Screen'],
        ]

        for url_extension, ptype in url_extensions:
            page_number = 0
            while True:
                url = url_base + '/catalogo/' + url_extension +\
                      '?pagina=' + str(page_number)

                soup = BeautifulSoup(browser.open(url).get_data())
                cells = soup.findAll('td', 'dd')

                if not cells:
                    break

                for cell in cells:
                    link = url_base + cell.find('a')['href']
                    product_links.append([link, ptype])
                page_number += 1

        return product_links
