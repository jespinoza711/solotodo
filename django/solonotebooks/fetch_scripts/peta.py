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

        product_name = product_soup.find('h1').string.encode('ascii', 'ignore').strip()

        try:
            product_price = int(product_soup.find('span', 'price').string.split('$')[1].replace('.', ''))
        except AttributeError:
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
            ['computadores/moviles/notebooks.html', 'Notebook'],
            ['computadores/moviles/netbooks.html', 'Notebook'],
            ['computadores/moviles/ultrabooks.html', 'Notebook'],
            ['apple.html', 'Notebook'],
            ['partes-y-piezas/display/tarjetas-de-video.html', 'VideoCard'],
            ['partes-y-piezas/componentes/procesadores.html', 'Processor'],
            ['partes-y-piezas/display/monitores.html', 'Screen'],
            ['partes-y-piezas/componentes/placas-madre.html', 'Motherboard'],
            ['partes-y-piezas/almacenamiento/memorias.html', 'Ram'],
            ['partes-y-piezas/almacenamiento/discos-duros.html', 'StorageDrive'],
            ['partes-y-piezas/componentes/fuentes-de-poder.html', 'PowerSupply'],
            ['partes-y-piezas/componentes/gabinetes.html', 'ComputerCase'],
            ['audio-y-video/televisores.html', 'Screen'],
        ]

        product_links = {}
        for url_extension, ptype in url_extensions:

            url = 'http://www.peta.cl/' + url_extension
            page_number = 1

            break_flag = False
            partial_links = {}

            while True:
                complete_url = url + '?limit=36&p=' + str(page_number)

                soup = BeautifulSoup(browser.open(complete_url).get_data())
                soup = soup.find('div', 'category-products')

                p_cells = []
                p_cells.extend(soup.findAll('li', {'class': 'item first'}))
                p_cells.extend(soup.findAll('li', {'class': 'item'}))
                p_cells.extend(soup.findAll('li', {'class': 'item last'}))

                for cell in p_cells:
                    link = cell.find('a')['href']
                    if link in partial_links:
                        break_flag = True
                        break
                    partial_links[link] = ptype

                if break_flag:
                    break
                page_number += 1

            product_links.update(partial_links)

        return product_links.items()

