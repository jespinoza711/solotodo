#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Peta(FetchStore):
    name = 'Peta'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link, already_tried = False):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except Exception:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)
        product_soup = BeautifulSoup(product_data)
        
        try:
            product_availability = product_soup.find('p', { 'class': 'availability in-stock' }).find('span')
            if product_availability.string and product_availability.string != 'En existencia':
                return None
        except Exception:
            return None
        
        try:
            product_name = product_soup.find('h1', { 'class': 'p-title' }).string.encode('ascii', 'ignore')
            product_price = int(product_soup.find('span', { 'class': 'price' }).string.split('$')[1].replace('.', ''))
        except Exception:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        browser = mechanize.Browser()

        url_extensions = [
            ['computadores-1/netbooks.html', 'Notebook'],
            ['computadores-1/notebooks.html', 'Notebook'],
            ['computadores-1/apple.html?appletype=898,903', 'Notebook'],
            ['peta-cl/tarjetas-de-video.html', 'VideoCard'],
            ['peta-cl/procesadores.html', 'Processor'],
            ['peta-cl/monitores.html', 'Monitor'],
            ['audio-y-video-1/televisores.html', 'Television'],
            ['peta-cl/placas-madre-1.html', 'Motherboard'],
            ['partes-y-piezas/memorias.html', 'Ram'],
            ['partes-y-piezas/discos-duros.html', 'StorageDrive'],
            ['partes-y-piezas/fuentes-de-poder.html', 'PowerSupply'],
        ]

        product_links = []
        for url_extension, ptype in url_extensions:

            url = 'http://www.peta.cl/' + url_extension
            first_page_url = url + '?limit=36&p=1'

            soup = BeautifulSoup(browser.open(first_page_url).get_data())

            page_count = soup.find('div', {'class': 'pages'})
            if page_count:
                page_count = int(page_count.findAll('a')[-2].string)
            else:
                page_count = 1

            for page_number in range(page_count):
                page_number += 1
                complete_url = url + '?limit=36&p=' + str(page_number)

                soup = BeautifulSoup(browser.open(complete_url).get_data())
                soup = soup.find('div', 'category-products')

                p_cells = []
                p_cells.extend(soup.findAll('li', {'class': 'item first'}))
                p_cells.extend(soup.findAll('li', {'class': 'item'}))
                p_cells.extend(soup.findAll('li', {'class': 'item last'}))

                for cell in p_cells:
                    link = cell.find('a')['href']

                    product_links.append([link, ptype])

        return product_links

