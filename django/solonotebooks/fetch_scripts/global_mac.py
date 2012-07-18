#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

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

        product_name = soup.find('h1').string.encode('ascii', 'ignore')
        product_price = soup.find('span', {'id': 'product_price'})

        if not product_price:
            return None

        product_price = int(clean_price_string(product_price.string))

        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

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
            ['home.php?cat=51', 'Notebook'],
            ['home.php?cat=52', 'Notebook'],
            ['home.php?cat=156', 'Notebook'],
            ['home.php?cat=47', 'Monitor'],
            ['home.php?cat=87', 'Monitor'],
            ['home.php?cat=81', 'StorageDrive'],
            ['home.php?cat=84', 'StorageDrive'],
        ]

        memory_catalog_url = url_base + 'home.php?cat=7'
        base_data = browser.open(memory_catalog_url).get_data()
        soup = BeautifulSoup(base_data)
        subcats = soup.findAll('span', 'subcategories')
        for subcat in subcats:
            link = subcat.find('a')['href'].replace(url_base, '')
            url_extensions.append([link, 'Ram'])

        product_links = []

        for url_extension, ptype in url_extensions:
            url = url_base + url_extension

            base_data = browser.open(url).get_data()
            soup = BeautifulSoup(base_data)

            titles = soup.findAll('a', 'product-title')

            for title in titles:
                product_links.append([title['href'], ptype])

        return product_links
