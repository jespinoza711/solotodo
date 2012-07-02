#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from django.utils.http import urlquote

class Bym(FetchStore):
    name = 'Bym'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link, already_tried = False):
        try:
            base_data = mechanize.urlopen(product_link)
        except Exception:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)

        base_soup = BeautifulSoup(base_data)

        title = base_soup.find('div', 'textTituloProducto')
        title = title.string.strip().encode('ascii', 'ignore')

        image = base_soup.findAll('div', 'textOtrosPrecios')[2]
        image = image.find('img')['src']
        if 'agotado' in image or 'proximo' in image:
            return None

        cash_price = base_soup.find('div', 'textPrecioContado')
        cash_price = int(cash_price.string.replace('$', '').replace('.', ''))

        product_data = ProductData()
        product_data.custom_name = title
        product_data.price = cash_price
        product_data.url = product_link.split('&osCsid')[0]
        product_data.comparison_field = product_data.url

        return product_data

    def retrieve_product_links(self):
        url_base = 'http://www.ttchile.cl/'
        product_urls_and_types = []

        url_extensions = [
            ['subpro.php?ic=21&isc=20', 'Notebook'],    # Notebooks
            ['catpro.php?ic=31', 'VideoCard'],          # Tarjetas de video
            ['catpro.php?ic=25', 'Processor'],          # Procesadores AMD
            ['catpro.php?ic=26', 'Processor'],          # Procesadores Intel
            ['catpro.php?ic=18', 'Screen'],             # LCD
            ['catpro.php?ic=23', 'Motherboard'],        # MB AMD
            ['catpro.php?ic=24', 'Motherboard'],        # MB Intel
            ['subpro.php?ic=16&isc=10', 'Ram'],         # RAM DDR
            ['subpro.php?ic=16&isc=11', 'Ram'],         # RAM DDR2
            ['subpro.php?ic=16&isc=12', 'Ram'],         # RAM DDR3
            ['subpro.php?ic=16&isc=13', 'Ram'],         # RAM Notebook
            ['subpro.php?ic=10&isc=4', 'StorageDrive'],  # HDD IDE
            ['subpro.php?ic=10&isc=6', 'StorageDrive'],  # HDD Notebook
            ['subpro.php?ic=10&isc=5', 'StorageDrive'],  # HDD SATA
            ['subpro.php?ic=10&isc=7', 'StorageDrive'],  # SSD
            ['catpro.php?ic=12', 'PowerSupply'],        # Fuentes de poder
            ['catpro.php?ic=13', 'ComputerCase'],        # Gabinetes
        ]

        for url_extension, ptype in url_extensions:
            page_number = 1

            while True:
                url = url_base + url_extension + '&pagina=' +\
                      str(page_number)
                base_data = mechanize.urlopen(url)
                base_soup = BeautifulSoup(base_data)

                divs = base_soup.findAll('div', 'linkTitPro')
                product_links = [div.find('a')['href'] for div in divs]

                if not product_links:
                    break

                for product_link in product_links:
                    url = url_base + product_link
                    product_urls_and_types.append([url, ptype])

                page_number += 1

        return product_urls_and_types

