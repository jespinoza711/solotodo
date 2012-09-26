#!/usr/bin/env python
from urllib2 import URLError

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
import re

class Falabella(FetchStore):
    name = 'Falabella'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()

        try:
            product_data = browser.open(product_link).get_data()
        except URLError:
            return None

        product_soup = BeautifulSoup(product_data)

        pn = product_soup.find('div',
                {'id': 'destacadoRuta'})

        if not pn:
            return None

        pn = pn.find('a').string

        try:
            pn = pn.replace('&nbsp;', ' ').replace('\r', ' ').replace('\n', ' ')
        except AttributeError:
            return None

        pn = ' '.join(re.split('\s+', pn.replace('\t', ' ')))
        product_name = pn.encode('ascii', 'ignore')

        product_price = int(product_soup.find('div', { 'class' : 'precio1' }).contents[2].replace('.', ''))
            
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        
        # Browser initialization
        browser = mechanize.Browser()

        base_url = ''\
                   'http://www.falabella.com/falabella-cl/browse/productList.jsp?'\
                   '_dyncharset=iso-8859-1&requestChainToken=0422806850&pageSize=16&'\
                   'priceFlag=&categoryId=cat{0}&docSort=numprop&docSortProp=price'\
                   '&docSortOrder=ascending&onlineStoreFilter=online&'\
                   'userSelectedFormat=4*4&trail=SRCH%3Acat{0}&navAction=jump&'\
                   'searchCategory=true&question=cat{0}&qfh_s_s=submit&_D%3Aqfh_s_s'\
                   '=+&qfh_ft=SRCH%3Acat{0}&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2F'\
                   'browse%2FfacetsFunctions.jsp.searchFacetsForm&goToPage='

        url_schemas = [
            ['70057', 'Notebook'],
            ['70054', 'Notebook'],
            ['1000006', 'Notebook'],
            ['2053', 'Television'],
            ['70043', 'Television'],
            ['70044', 'Television'],
            ]

        product_links = []
                            
        for url_schema, ptype in url_schemas:
            page_number = 1
            
            while True:
                url = base_url.format(url_schema) + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(url).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                mosaicDivs = baseSoup.findAll('div', { 'class':'quickView' })
                
                if not mosaicDivs:
                    break
                
                for div in mosaicDivs:                        
                    url = 'http://www.falabella.com' + div.find('a')['href']
                    url = url.replace(' ', '')
                    
                    m = re.search(';jsessionid=\S+\.node\d', url)
                    if m:
                        url = url[:m.start()] + url[m.end():]

                    url = ''.join(url.split())
                    product_links.append([url, ptype])
                    
                page_number += 1
        
        return product_links

