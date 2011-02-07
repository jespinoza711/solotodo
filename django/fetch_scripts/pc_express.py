#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class PCExpress:
    name = 'PC Express'

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, product_link):
        br = mechanize.Browser()
        data = br.open(product_link).get_data()
        soup = BeautifulSoup(data)
        productData = ProductData()

        title = soup.findAll('b')[2].string
        
        price = int(soup.find('font', {'size':'3'}).find('span').contents[1].string.replace('$', '').replace(',', ''))

        productData.custom_name = title
        productData.price = price
        productData.url = product_link
        productData.comparison_field = product_link
        print productData
        return productData


    # Main method
    def getNotebooks(self):
        print 'Getting PCExpress notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.pc-express.cl/index.php?cPath='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  
                            '75_136',
                        ]
                            
        product_links = []
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            td_products = baseSoup.findAll('td', { 'class' : 'wrapper_pic_br wrapper_pic_td' })
            
            
            for td_product in td_products:
                link = td_product.find('a')['href']
                product_links.append(link)

                    
        for product_link in product_links:
            prod = self.retrieve_product_data(product_link)
            if prod:
                productsData.append(prod)
                    

        return productsData
