#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.fetch_scripts.utils import clean_price_string

class GlobalMac(FetchStore):
    name = 'GlobalMac'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (MyProgram/0.1)'),
                             ('From', 'responsible.person@example.com')]
        mechanize.install_opener(opener)
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        soup = BeautifulSoup(product_data)

        product_name = soup.find('title').string.encode('ascii', 'ignore')

        product_prices = soup.find('div', 'price').contents

        try:
            cash_price = int(clean_price_string(product_prices[4]))

            product_data = ProductData()
            product_data.custom_name = product_name
            product_data.price = cash_price
            product_data.url = product_link
            product_data.comparison_field = product_link

            return product_data
        except IndexError:
            return None

    # Main method
    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (MyProgram/0.1)'),
                             ('From', 'responsible.person@example.com')]
        mechanize.install_opener(opener)
        url_base = 'http://www.globalmac.cl/'

        browser = mechanize.Browser()

        url_extensions = [
            ['Distribuidor-Apple-Chile/MacBook-Air', 'Notebook'],
            ['Distribuidor-Apple-Chile/MacBook-Pro', 'Notebook'],
            ['Hardware-Mac-PC/Discos-Duros-Notebook-SATA-2.5', 'StorageDrive'],
            ['Hardware-Mac-PC/Discos-Duros-SATA-3.5', 'StorageDrive'],
            ['Hardware-Mac-PC/Discos-Duros-SSD-SATA-2.5', 'StorageDrive'],
            ]

        product_links = []

        for url_extension, ptype in url_extensions:
            url = url_base + url_extension
            base_data = browser.open(url).get_data()
            soup = BeautifulSoup(base_data)

            for item in soup.findAll('div', 'name'):
                product_links.append([item.find('a')['href'], ptype])

        return product_links
