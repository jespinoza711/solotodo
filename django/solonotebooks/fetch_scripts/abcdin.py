#!/usr/bin/env python

import mechanize
from mechanize import HTTPError
import re
import htmlentitydefs
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace('&quot;', '"')
    s = s.replace('&apos;', "'")
    s = s.replace("&amp;", "&")
    return s

class AbcDin(FetchStore):
    name = 'AbcDin'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        product_details_url = product_link.split('#')[1]
        try:
            product_webpage = mechanize.urlopen(product_details_url)
        except HTTPError, e:
            return None
        product_soup = BeautifulSoup(product_webpage.read())
        
        av_span = product_soup.find('div', { 'id': 'caja-compra' }).find('span')
        if av_span:
            return None
        
        product_name = product_soup.find('td', { 'id': 'mainDescr' }).find('h2').contents[0].encode('ascii', 'ignore')
        try:
            product_price = int(product_soup.find('div', { 'id': 'precioProducto' }).find('strong').string.replace('Precio Internet: $', '').replace(',', ''))
        except:
            product_price = int(product_soup.find('div', { 'id': 'precioNormal' }).find('span').string.replace('$', '').replace(',', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.url = product_link
        product_data.price = product_price
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        
        xml_resources = [
                    'notebooks',
                    'netbooks',
                    'LCD',
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
                
        return product_links
