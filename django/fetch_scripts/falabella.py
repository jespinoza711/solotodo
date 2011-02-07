#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Falabella:
    name = 'Falabella'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'id' : 'descripcion-corta' }).find('h1').string.encode('ascii', 'ignore')
        
        product_price = None
        try:
            product_price = int(product_soup.find('div', { 'id' : 'precioNormalF' }).string.split('&#36;')[1].replace('.', ''))
        except:
            pass
            
        if not product_price:
            try:
                product_price = int(product_soup.find('div', { 'id' : 'precioInternetF' }).string.split('&#36;')[1].replace('.', ''))
            except:
                pass
            
        if not product_price:
            try:
                product_price = int(product_soup.find('div', { 'id' : 'precioInternetRF' }).string.split('&#36;')[1].replace('.', ''))
            except:
                pass
            
        if not product_price:
            try:
                product_price = int(product_soup.find('div', { 'id' : 'oportunidadF' }).string.split('&#36;')[1].replace('.', ''))
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
    def getNotebooks(self):
        print 'Getting Falabella notebooks'
        # Basic data of the target webpage and the specific catalog
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_schemas = [    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=[page]&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                            
 ]
        product_links = []
                            
        for url_schema in url_schemas:
            page_number = 0
            
            while True:
                url = url_schema.replace('[page]', str(page_number))

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(url).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                mosaicDivs = baseSoup.findAll("div", { "id" : "mosaico" })
                
                if not mosaicDivs:
                    break
                
                for mosaicDiv in mosaicDivs:                        
                    url = 'http://www.falabella.com' + mosaicDiv.find('a')['href']
                    product_links.append(url)
                    
                page_number += 1
        
        for product_link in product_links:
            products_data.append(self.retrieve_product_data(product_link))
        
        return products_data

