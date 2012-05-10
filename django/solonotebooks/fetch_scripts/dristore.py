#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore


class Dristore(FetchStore):
    name = 'Dristore'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        soup = BeautifulSoup(mechanize.urlopen(product_link))
        
        if soup.find('span', 'warning_inline'):
            return None

        product_data = ProductData()
        
        title = soup.find('h1').string.strip().encode('ascii', 'ignore')
        
        price = soup.find('span', {'id': 'our_price_display'}).string
        price = int(price.replace('.', '').replace('$', ''))

        product_data.custom_name = title
        product_data.price = price
        product_data.url = product_link
        product_data.comparison_field = product_data.url	 
        
        return product_data

    def retrieve_product_links(self):
        product_urls_and_types = {}
        
        url_extensions = [
            ['33-discos-duros', 'StorageDrive'],
            ['28-fuentes-de-poder', 'PowerSupply'],
            ['47-gabinetes', 'ComputerCase'],
            ['29-memorias-ram', 'Ram'],
            ['55-monitores', 'Screen'],
            ['54-procesadores', 'Processor'],
            ['52-tarjetas-de-video', 'VideoCard'],
        ]
                            
        for url_extension, ptype in url_extensions:
            p = 1

            while True:
                url = 'http://www.dristore.cl/catalogo/' + url_extension + '?p=' + str(p)
                base_soup = BeautifulSoup(mechanize.urlopen(url))

                product_urls = [li.find('a')['href'] for li in base_soup.findAll('li', 'ajax_block_product')]

                flag = False

                for url in product_urls:
                    if url in product_urls_and_types:
                        flag = True
                        break
                    product_urls_and_types[url] = ptype

                if flag:
                    break

                p += 1

        return product_urls_and_types.items()

