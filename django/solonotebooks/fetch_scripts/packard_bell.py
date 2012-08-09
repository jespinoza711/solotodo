#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PackardBell(FetchStore):
    name = 'Packard Bell'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        soup = BeautifulSoup(product_data)

        name = soup.find('div', 'dnombre_producto').string
        name = name.encode('ascii', 'ignore').strip()

        if soup.find('div', 'dboton_sinstock'):
            return None

        price = soup.find('div', 'dprecio_oferta').contents[1]
        price = int(price.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = name
        product_data.price = price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        browser = mechanize.Browser()

        url_extensions = [
            ['151-Ultrabook.html', 'Notebook'],
            ['127-Notebooks.html', 'Notebook'],
            ['128-Netbooks.html', 'Notebook'],
            ['146-Monitores.html', 'Screen'],
        ]

        product_links = []
        for url_extension, ptype in url_extensions:
            url = 'http://www.netnow.cl/catalogo/' + url_extension

            soup = BeautifulSoup(browser.open(url).get_data())
            links = soup.findAll('a', 'Producto_Detalles')

            for link in links:
                url = link['href']
                product_links.append([url, ptype])

        return product_links

