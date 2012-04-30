#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

class PortatilChile(FetchStore):
    name = 'PortatilChile'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)

        try:
            name = product_soup.find('th', {'colspan': '2'}).string
        except AttributeError:
            return None
        name = name.encode('ascii', 'ignore').split('"')[1]

        prices = {}

        cash_price = product_soup.find('table',
                {'cellspacing': '1'}).find('table')
        cash_price = cash_price.findAll('td')[3].find('strong').string
        cash_price = int(clean_price_string(cash_price))

        for p in ['cash', 'deposit', 'wire_transfer']:
            prices[p] = cash_price
        product_data = ProductData()
        product_data.custom_name = name
        product_data.price = cash_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        urlBase = 'http://www.portatilchile.cl/productos.html'

        browser = mechanize.Browser()
        soup = BeautifulSoup(browser.open(urlBase).get_data())

        product_tables = soup.findAll('table', {'width': '226'})

        product_links = []

        for product_table in product_tables:
            link = product_table.find('a')['href']
            product_links.append([link, 'Notebook'])

        return product_links
