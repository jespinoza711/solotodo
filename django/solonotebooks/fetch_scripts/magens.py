#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

class Magens(FetchStore):
    name = 'Magens'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()

        try:
            product_soup = BeautifulSoup(product_data)
        except UnicodeEncodeError:
            return None

        name = product_soup.find('div', {'class': 'titleContent'}).string
        name = name.encode('ascii', 'ignore')

        try:
            availability = product_soup.find('div', {'class': 'stock'})
            availability = availability.contents[4]
        except AttributeError:
            return None

        if 'Agotado' in availability:
            return None

        cash_price = product_soup.findAll('div', {'class': 'precioDetalle'})[-1]
        cash_price = cash_price.string.split('$')[1]
        cash_price = int(clean_price_string(cash_price))

        part_number = product_soup.find('div', { 'class': 'codProduct' }).string.replace('[', '').replace(']', '').encode('ascii', 'ignore').strip()

        product_data = ProductData()
        product_data.custom_name = name
        product_data.price = cash_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        product_data.part_number = part_number
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        browser = mechanize.Browser()

        url_extensions = [
            ['promo-notebooks-c-15_449.html', 'Notebook'],
            ['notebooks-c-15_202.html', 'Notebook'],
            ['notebooks-c-15_203.html', 'Notebook'],
            ['netbooks-c-15_199.html', 'Notebook'],
            ['notebooks-c-15_204.html', 'Notebook'],
            ['notebooks-mas-c-15_205.html', 'Notebook'],
            ['nvidia-festi-game-c-24_448.html', 'VideoCard'],
            ['video-pcie-ati-c-24_130.html', 'VideoCard'],
            ['video-pcie-nvidia-c-24_129.html', 'VideoCard'],
            ['video-profesionales-c-24_131.html', 'VideoCard'],
            ['procesadores-c-1.html', 'Processor'],
            ['monitores-lcd-c-13_90.html', 'Screen'],
            ['monitores-led-c-13_200.html', 'Screen'],
            ['televisores-ledtv-c-13_210.html', 'Screen'],
            ['televisores-lcdtv-c-13_91.html', 'Screen'],
            ['placas-madre-c-2.html', 'Motherboard'],
            ['memorias-c-12.html', 'Ram'],
            ['discos-duros-c-3_35.html', 'StorageDrive'],
            ['ssd-c-3_215.html', 'StorageDrive'],
            ['discos-notebook-c-3_37.html', 'StorageDrive'],
            ['fuentes-poder-c-10_76.html', 'PowerSupply'],
            ['gabinetes-con-fuente-c-10_75.html', 'ComputerCase'],
            ['gabinetes-sin-fuente-c-10_299.html', 'ComputerCase'],
        ]

        product_links = []
        for url_extension, ptype in url_extensions:
            url = 'http://www.magens.cl/' + url_extension +\
                  '?mostrar=1000'

            soup = BeautifulSoup(browser.open(url).get_data())

            product_containers = soup.findAll('div', 'modulProducto')
            for container in product_containers:
                link = container.find('a')['href']
                print link
                product_links.append([link, ptype])

        return product_links