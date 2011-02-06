#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Bym:
    name = 'Bym'

    # Main method
    def getNotebooks(self):
        print 'Getting Bym notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ttchile.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  
                            'subpro.php?idCat=21&idSubCat=20',
                            ]
                            
        for url_extension in url_extensions:
            page_number = 1
            
            while True:
                urlWebpage = urlBase + url_extension + '&pagina=' + str(page_number)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                productLinks = [div.find('a')['href'] for div in baseSoup.findAll('div', {'class': 'linkTitPro'})]
                
                if not productLinks:
                    break
                
                for productLink in productLinks:
                    urlProduct = urlBase + productLink
                    
                    baseData = browser.open(urlProduct).get_data()
                    baseSoup = BeautifulSoup(baseData)
                    
                    productData = ProductData()
                    
                    stock_image_url = baseSoup.findAll('div', { 'class' : 'textOtrosPrecios' })[2].find('img')['src']
                    if 'agotado' in stock_image_url:
                        continue;
                    
                    title = baseSoup.find('div', { 'class' : 'textTituloProducto'}).string.strip()
                    
                    prices = baseSoup.findAll('div', { 'class' : 'textOtrosPrecios' })
                    price = prices[0].string
                    price = int(price.replace('.', '').replace('$', ''))

                    productData.custom_name = title
                    productData.price = price
                    productData.url = urlProduct.split('&osCsid')[0]
                    productData.comparison_field = productData.url	    	    
                    productsData.append(productData)
                    
                    print productData
                
                page_number += 1

        return productsData

