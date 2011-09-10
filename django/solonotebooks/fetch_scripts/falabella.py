#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore
import re

class Falabella(FetchStore):
    name = 'Falabella'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'id' : 'destacadoRuta' }).find('a').string

        if not product_name:
            return None

        product_name = ' '.join(re.split('\s+', product_name.replace('&nbsp;', ' ').replace('\r', ' ').replace('\n', ' ').replace('\t', ' '))).encode('ascii', 'ignore')

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
        
        url_schemas = [    
                            ['http://www.falabella.com/falabella-cl/browse/productList.jsp?_dyncharset=iso-8859-1&requestChainToken=0005653415&pageSize=16&priceFlag=&categoryId=cat70057&docSort=numprop&docSortProp=price&docSortOrder=ascending&onlineStoreFilter=online&userSelectedFormat=4*4&trail=SRCH%3Acat70057&navAction=jump&searchCategory=true&question=cat70057&qfh_s_s=submit&_D%3Aqfh_s_s=+&qfh_ft=SRCH%3Acat70057&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2Fbrowse%2FfacetsFunctions.jsp&goToPage=', 'Notebook'],
                            ['http://www.falabella.com/falabella-cl/browse/productList.jsp?_dyncharset=iso-8859-1&requestChainToken=0005655243&pageSize=16&priceFlag=&categoryId=cat70043&docSort=numprop&docSortProp=price&docSortOrder=ascending&onlineStoreFilter=online&userSelectedFormat=4*4&trail=SRCH%3Acat70043&navAction=jump&searchCategory=true&question=cat70043&qfh_s_s=submit&_D%3Aqfh_s_s=+&qfh_ft=SRCH%3Acat70043&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2Fbrowse%2FfacetsFunctions.jsp&goToPage=', 'Screen'],
                            ['http://www.falabella.com/falabella-cl/browse/productList.jsp?_dyncharset=iso-8859-1&requestChainToken=0005655389&pageSize=16&priceFlag=&categoryId=cat2053&docSort=numprop&docSortProp=price&docSortOrder=ascending&onlineStoreFilter=online&userSelectedFormat=4*4&trail=SRCH%3Acat2053&navAction=jump&searchCategory=true&question=cat2053&qfh_s_s=submit&_D%3Aqfh_s_s=+&qfh_ft=SRCH%3Acat2053&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2Fbrowse%2FfacetsFunctions.jsp&goToPage=', 'Screen'],
                            ['http://www.falabella.com/falabella-cl/browse/productList.jsp?_dyncharset=iso-8859-1&requestChainToken=0005655389&pageSize=16&priceFlag=&categoryId=cat70044&docSort=numprop&docSortProp=price&docSortOrder=ascending&onlineStoreFilter=online&userSelectedFormat=4*4&trail=SRCH%3Acat70044&navAction=jump&searchCategory=true&question=cat70044&qfh_s_s=submit&_D%3Aqfh_s_s=+&qfh_ft=SRCH%3Acat70044&_D%3Aqfh_ft=+&_DARGS=%2Ffalabella-cl%2Fbrowse%2FfacetsFunctions.jsp&goToPage=', 'Screen'],
                            
                      ]
        product_links = []
                            
        for url_schema, ptype in url_schemas:
            page_number = 1
            
            while True:
                url = url_schema + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(url).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                mosaicDivs = baseSoup.findAll('div', { 'class':'quickView' })
                
                if not mosaicDivs:
                    break
                
                for div in mosaicDivs:                        
                    url = 'http://www.falabella.com' + div.find('a')['href']
                    
                    product_links.append([url, ptype])
                    
                page_number += 1
        
        return product_links

