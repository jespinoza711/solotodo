#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class PCOfertas(FetchStore):
    name = 'PC Ofertas'
    use_existing_links = False
    blacklist = [
        'http://www.pcofertas.cl/index.php?route=product/category&path=74_147', # Memoria notebook
    ]
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        try:
            product_name = product_soup.find('h4', { 'class': 'Estilo5' }).string.encode('ascii', 'ignore')
        except:
            return None
        
        try:
            product_price = int(product_soup.find('span', { 'style': 'color: #F00; font-size:12px;' }).parent.parent.parent.findAll('td')[1].find('span').string.replace('$', '').replace(',', ''))
        except:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data
        
    def recursive_retrieve_product_links(self, url):
        browser = mechanize.Browser()
        baseData = browser.open(url).get_data()
        baseSoup = BeautifulSoup(baseData)
        product_links = []
        
        products_table = baseSoup.findAll('table', { 'class' : 'list' })
        if not products_table:
            return []
        elif len(products_table) == 2:
            # Page with categories
            
            # First get the products on the page
            products_anchor_tags = products_table[1].findAll('a')[::3]
            for anchor_tag in products_anchor_tags:
                link = anchor_tag['href']
                product_links.append(link)
            
            # Then the ones on sub categories
            category_links = products_table[0].findAll('a')[::2]
            for anchor_tag in category_links:
                link = anchor_tag['href']
                if link not in self.blacklist:
                    product_links.extend(self.recursive_retrieve_product_links(link))
        else:
            # Page mayy have only products or only category links
            products_anchor_tags = products_table[0].findAll('a')[::3]
            for anchor_tag in products_anchor_tags:
                link = anchor_tag['href']
                if 'product_id' in link:
                    product_links.append(link)
                else:
                    product_links.extend(self.recursive_retrieve_product_links(link))
        return product_links


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pcofertas.cl/index.php?route=product/category&path='
        
        product_links = []
        
        url_extensions = [  
                            ['74', 'Notebook'],   # Notebook
                            ['75', 'Notebook'],   # Netbook
                            ['87', 'VideoCard'],   # Tarjetas de video
                            ['18', 'Processor'],   # Procesadores
                            ['28', 'Screen'],   # Monitores
                            ['108', 'Motherboard'],   # Monitores
                            ]
        
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension
            links = self.recursive_retrieve_product_links(urlWebpage)

            links = list(set(links))
                
            for link in links:
                base_link, args = link.split('?')
                args = dict([elem.split('=') for elem in args.split('&')])
                del args['path']
                args = ['%s=%s' % (k, v) for k, v in args.items()]
                link = base_link + '?' + '&'.join(args)
                if link not in product_links:
                    product_links.append([link, ptype])

        return product_links

