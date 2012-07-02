#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore


class Sistemax(FetchStore):
    name = 'Sistemax'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.findAll('h2')[3].find('font').string.encode('ascii', 'ignore')
        product_price = int(product_soup.findAll('span', { 'class': 'style18' })[0].string)
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        base_url = 'http://www.sistemax.cl/webstore/'

        extensions = [
            ['112', 'Notebook'],     # Netbooks
            ['27', 'Notebook'],      # Notebooks
            ['35', 'VideoCard'],     # Tarjetas de video
            ['58', 'Processor'],     # Procesadores AMD
            ['59', 'Processor'],     # Procesadores Intel
            ['25', 'Screen'],       # Monitores
            ['125', 'Screen'],   # Televisores
            ['82', 'Notebook'],      # Mac / iPod
            ['30', 'Motherboard'],   # MB AMD
            ['69', 'Motherboard'],   # MB Intel
            ['24', 'Ram'],           # RAM
            ['16', 'StorageDrive'],  # Discos duros y SSD
            ['21', 'PowerSupply'],   # Fuentes de poder
            ['19', 'ComputerCase'],  # Gabinetes
        ]

        product_links = []
        for extension, ptype in extensions:
            url = base_url + 'index.php?op=seccion/id=' + extension +\
                  '&page=-1&listar=true'

            browser = mechanize.Browser()

            soup = BeautifulSoup(browser.open(url).get_data())
            info_cells = soup.findAll('td', {'scope': 'col'})

            url_cells = info_cells[3::5]
            urls = [base_url + url_cell.contents[2]['href']
                    for url_cell in url_cells]
            for url in urls:
                product_links.append([url, ptype])

        return product_links
