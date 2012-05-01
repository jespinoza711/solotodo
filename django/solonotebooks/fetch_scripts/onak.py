#!/usr/bin/env python
from httplib import BadStatusLine

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Onak(FetchStore):
    name = 'Onak'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        try:
            data = br.open(productUrl).get_data()
        except BadStatusLine:
            return None
        soup = BeautifulSoup(data)

        productData = ProductData()

        title = soup.findAll('h1')[1].string.strip()
        
        price = int(soup.findAll('span', 'price')[1].string.replace('$', '').replace('.', ''))

        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.onak.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        
        url_extensions = [
            ['pc-servidores/notebooks.html', 'Notebook'],
            ['pc-servidores/netbooks.html', 'Notebook'],
            ['almacenamiento/discos-duro.html', 'StorageDrive'],
            ['multimedia/televisores.html', 'Screen'],
            ['componentes/memorias-ram-1.html', 'Ram'],
            ['componentes/fuentes-poder.html', 'PowerSupply'],
            ['componentes/procesadores.html', 'Processor'],
            ['componentes/placas-madre.html', 'Motherboard'],
            ['componentes/tarjetas-video.html', 'VideoCard'],
            ['componentes/monitores.html', 'Screen'],
        ]
        
        product_urls = {}
        
        for url_extension, ptype in url_extensions:
            page_number = 1

            while True:
                url = urlBase + url_extension + '?limit=32&p=' + str(page_number)
                soup = BeautifulSoup(browser.open(url).get_data())

                product_table = soup.find('table', {'id': 'product-list-table'})
                product_paragraphs = product_table.findAll('p', 'product-image')

                done = False

                for p in product_paragraphs:
                    product_url = p.find('a')['href']
                    if product_url in product_urls:
                        done = True
                        break
                    product_urls[product_url] = ptype

                if done:
                    break

                page_number += 1

        return product_urls.items()

