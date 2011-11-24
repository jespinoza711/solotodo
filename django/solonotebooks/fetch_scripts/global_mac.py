#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class GlobalMac(FetchStore):
    name = 'GlobalMac'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h1').string.encode('ascii', 'ignore')
        try:
            product_price = int(product_soup.find('span', { 'id': 'product_price' }).string.replace('.', ''))
        except:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.globalmac.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['MacBook/', 'Notebook'],
                            ['MacBook-Pro/', 'Notebook'],
                            ['Cinema-Display/', 'Screen'],
                            ]
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)
            
            titles = baseSoup.findAll('a', {'class': 'product-title'})

            for title in titles:
            	product_links.append([title['href'], ptype])
            	
        return product_links

