#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Falabella(FetchStore):
    name = 'Falabella'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        avail_div = product_soup.find('div', { 'id' : 'mensajeSinStock' })
        if avail_div:
            return None
        
        product_name = product_soup.find('div', { 'id' : 'descripcion-corta' }).find('h1').string.encode('ascii', 'ignore')
        
        product_prices = []
        
        try:
            product_price = int(product_soup.find('div', { 'id' : 'precioNormalF' }).string.split('&#36;')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
        
        try:
            product_price = int(product_soup.find('div', { 'id' : 'precioInternetF' }).string.split('&#36;')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
        
        try:
            product_price = int(product_soup.find('div', { 'id' : 'precioInternetRF' }).string.split('&#36;')[1].replace('.', ''))
            product_prices.append(product_price)
        except:
            pass
            
        try:
            product_price = int(product_soup.find('div', { 'id' : 'oportunidadF' }).string.split('&#36;')[1].replace('.', ''))
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
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_schemas = [    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=[page]&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                           'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?sprod=0&ConFoto=1&cgmenbr=1891&nivel=1&cgrfnbr=2541581&sfot=0&cgpadre=2457964&cgnieto=2541581&cghijo1=2486170&division=[page]',
                            
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
                    base_url, args = url.split('?')
                    d_args = dict([elem.split('=') for elem in args.split('&')])
                    del d_args['division']
                    url = base_url + '?' + '&'.join([key + '=' + value for key, value in d_args.items()])
                    
                    product_links.append(url)
                    
                page_number += 1
        
        return product_links

