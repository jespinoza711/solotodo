#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData

class Peta:
    name = 'Peta'
    
    def retrieve_product_data(self, product_link, already_tried = False):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h3', { 'class': 'product-name' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'class': 'price' }).string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting Peta notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.peta.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  'computadores-1/netbooks.html',
                            'computadores-1/notebooks.html',
                            'peta-cl/tarjetas-de-video.html',
                            'peta-cl/procesadores.html',
                            'peta-cl/monitores.html',
                            ]
                          
        product_links = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension
            pageNumber = 1
                
            while True:
                completeWebpage = urlWebpage + '?p=' + str(pageNumber)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                ntbkCells = baseSoup.find('table', { 'id': 'product-list-table'})
                if not ntbkCells:
                    break
                
                ntbkCells = ntbkCells.findAll('td')

                trigger = False
                for ntbkCell in ntbkCells:
                    try:
                        link = ntbkCell.findAll('a')[1]
                    except:
                        break
                        
                    link = link['href']
                    if link in product_links:
                        trigger = True
                        break
                    product_links.append(link)
                    
                if trigger:
                    break
                    
                pageNumber += 1
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data

