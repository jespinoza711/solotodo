#!/usr/bin/env python

import mechanize
import re
import htmlentitydefs
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace('&quot;', '"')
    s = s.replace('&apos;', "'")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s


class AbcDin:
    name = 'AbcDin'
    
    def retrieve_product_data(self, product_link):
        product_details_url = product_link.split('#')[1]
        product_webpage = mechanize.urlopen(product_details_url)
        product_soup = BeautifulSoup(product_webpage.read())
        
        product_name = product_soup.find('td', { 'id': 'mainDescr' }).find('h2').contents[0].encode('ascii', 'ignore')
        try:
            product_price = int(product_soup.find('div', { 'id': 'precioNormal' }).find('span').string.replace('$', '').replace(',', ''))
        except:
            product_price = int(product_soup.find('div', { 'id': 'precioProducto' }).find('strong').string.replace('Precio Internet: $', '').replace(',', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.url = product_link
        product_data.price = product_price
        product_data.comparison_field = product_link
        
        print product_data
        
        return product_data

    # Main method
    def get_products(self):
        print 'Getting AbcDin notebooks'
        
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        
        # Array containing the data for each product
        products_data = []
        
        xml_resources = [
                    'notebooks',
                    'netbooks',
                        ]
                        
        product_links = []
                        
        for xml_resource in xml_resources:
            # Obtain and parse HTML information of the base webpage
            base_data = mechanize.urlopen('https://www.abcdin.cl/abcdin/catabcdin.nsf/%28webProductosxAZ%29?readviewentries&restricttocategory=' + xml_resource)
            base_soup = BeautifulSoup(base_data.read())

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            ntbks_data = base_soup.findAll('text')
            
            for ntbk_data in ntbks_data:
                ntbk_data = unescape(ntbk_data.contents[0])
                temp_soup = BeautifulSoup(ntbk_data)
                div = temp_soup.find('div')
                link = 'https://www.abcdin.cl/abcdin/abcdin.nsf#https://www.abcdin.cl' + div.find('a')['href']
                product_links.append(link)
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            products_data.append(product)
                
        return products_data

