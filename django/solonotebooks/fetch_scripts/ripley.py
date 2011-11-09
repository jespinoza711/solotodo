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
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ripley.cl/webapp/wcs/stores/servlet/'
        
        category_urls = [
            ['categoria-TVRipley-10051-001772-130000-ESP-N--', 'Notebook'],   # Notebooks
            ['categoria-TVRipley-10051-001830-130000-ESP-N--', 'Notebook'],   # Netbooks
            ['categoria-TVRipley-10051-013040-230000-ESP-N', 'Screen'],     # LCDs
                        ]
        
        # Browser initialization
        browser = mechanize.Browser()
        
        product_links = []
        links = []
        
        for category_url, ptype in category_urls:
            j = 1                    
            while True:
                urlWebpage = urlBase + category_url + '?curPg=' + str(j)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                productParagraphs = baseSoup.findAll('td', { 'class' : 'grisCatalogo' })
                productParagraphs = productParagraphs[1::3]
                productParagraphs = [pp.parent.parent for pp in productParagraphs]
                
                if not productParagraphs:
                    break
                    
                break_flag = False
                    
                for p in productParagraphs:
                    url = urlBase + p.find('a')['href']
                    
                    if url in links:
                        break_flag = True
                        break
                        
                    url = url.encode('ascii', 'ignore')
                    links.append(url)
                    product_links.append([url, ptype])
                    
                if break_flag:
                    break
                    
                j += 1          

        return product_links

