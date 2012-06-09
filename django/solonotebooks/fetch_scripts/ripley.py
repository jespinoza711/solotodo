#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Ripley(FetchStore):
    name = 'Ripley'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        
        product_data = browser.open(product_link).get_data()
    
        product_soup = BeautifulSoup(product_data)
        
        try:
            product_name = product_soup.find('span', { 'class': 'textogrisbold' }).string.encode('ascii', 'ignore')
        except AttributeError, e:
            return None
        
        product_prices = []
        
        
        try:
            product_price = int(product_soup.find('span', { 'class': 'normalHOME' }).string.replace('$', '').replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
            
        try:
            product_price = int(product_soup.find('div', { 'class': 'textodetallesrojo' }).find('div').string.split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
            
        try:
            product_price = int(product_soup.find('div', { 'class': 'textodetallesrojo' }).string.split('$')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
                
        if not product_prices:
            raise Exception
            
        product_price = min(product_prices)
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        url_base = 'http://www.ripley.cl/webapp/wcs/stores/servlet/'

        category_urls = [
            ['categoria-TVRipley-10051-001772-130000-ESP-N--', 'Notebook'],
            ['categoria-TVRipley-10051-001860-130000-ESP-N--', 'Notebook'],
            ['categoria-TVRipley-10051-013040-230000-ESP-N', 'Screen'],
        ]

        browser = mechanize.Browser()

        product_links = {}

        for category_url, ptype in category_urls:
            j = 1
            while True:
                url = url_base + category_url + '?curPg=' + str(j)

                soup = BeautifulSoup(browser.open(url).get_data())

                p_paragraphs = soup.findAll('td', {'class': 'grisCatalogo'})
                p_paragraphs = p_paragraphs[1::3]
                p_paragraphs = [pp.parent.parent for pp in p_paragraphs]

                for p in p_paragraphs:
                    url = url_base + p.find('a')['href']
                    url = url.encode('ascii', 'ignore')
                    if url not in product_links:
                        product_links[url] = ptype

                next_page_link = soup.findAll('a',
                        {'class': 'linknormal4'})[-1]
                if next_page_link.string.strip() != '&gt;&gt;':
                    break

                j += 1

        return product_links.items()

