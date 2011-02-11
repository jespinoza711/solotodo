#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Ripley:
    name = 'Ripley'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('span', { 'class': 'textogrisbold' }).string.encode('ascii', 'ignore')
        
        product_price = None
        
        try:
            product_price = int(product_soup.find('span', { 'class': 'normalHOME' }).string.replace('$', '').replace('.', ''))
        except:
            pass
            
        if not product_price:
            try:
                product_price = int(product_soup.find('div', { 'class': 'textodetallesrojo' }).find('div').string.split('$')[1].replace('.', ''))
            except:
                pass
                
        if not product_price:
            raise Exception
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting Ripley notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ripley.cl/webapp/wcs/stores/servlet/'
        
        category_urls = [
            'categoria-TVRipley-10051-001772-130000-ESP-N--',
                        ]
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        product_links = []
        
        for category_url in category_urls:
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
                    
                    if url in product_links:
                        break_flag = True
                        break
                        
                    product_links.append(url)
                    
                if break_flag:
                    break
                    
                j += 1          

        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

