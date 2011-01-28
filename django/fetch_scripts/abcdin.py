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

    # Main method
    def getNotebooks(self):
        print 'Getting AbcDin notebooks'
        
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        
        # Array containing the data for each product
        productsData = []
        
        xml_resources = [
                    'https://www.abcdin.cl/abcdin/catabcdin.nsf/%28webProductosxAZ%29?readviewentries&restricttocategory=notebooks',
                    'https://www.abcdin.cl/abcdin/catabcdin.nsf/%28webProductosxAZ%29?readviewentries&restricttocategory=netbooks'
                        ]
                        
        for xml_resource in xml_resources:
            # Obtain and parse HTML information of the base webpage
            baseData = mechanize.urlopen(xml_resource)
            baseSoup = BeautifulSoup(baseData.read())

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            ntbks_data = baseSoup.findAll('text')
            
            for ntbk_data in ntbks_data:
                ntbk_data = unescape(ntbk_data.contents[0])
                temp_soup = BeautifulSoup(ntbk_data)
                div = temp_soup.find('div')
                link = 'https://www.abcdin.cl/abcdin/abcdin.nsf#https://www.abcdin.cl' + div.find('a')['href']
                name = div.find('div', {'class': 'txt_pod'}).string.encode('ascii', 'ignore')
                price = int(div.find('div', {'class': 'precio_pod'}).string.replace('$', '').replace('.', ''))
                product_data = ProductData();
                product_data.custom_name = name
                product_data.url = link
                product_data.price = price
                product_data.comparison_field = link
                print product_data
                productsData.append(product_data)
                
        return productsData

