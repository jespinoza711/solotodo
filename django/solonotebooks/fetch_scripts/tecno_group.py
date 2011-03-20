#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class TecnoGroup(FetchStore):
    name = 'TecnoGroup'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h3').contents[0]
        product_price = int(product_soup.find('h3').parent.findAll('div')[3].string.split('$')[1].split('IVA')[0].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.tecnogroup.cl/'
        urlBuscarProductos = 'index.php?cPath='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['2_35', 'Notebook'],
                            ['2_81', 'Notebook'],
                            ['2_117', 'Notebook'],
                            ['2_33', 'Notebook'],
                            ['2_43', 'Notebook'],
                            ['2_10', 'Notebook'],
                            ['2_11', 'Notebook'],
                            ['2_13', 'Notebook'],
                            ['2_34', 'Notebook'],
                            ['4_44', 'Notebook'],
                            ['4_139', 'Notebook'],
                            ['4_47', 'Notebook'],
                            ['4_48', 'Notebook'],
                            ['4_49', 'Notebook'],
                            ['4_109', 'Notebook'],
                            ['4_45', 'Notebook'],
                            ['4_46', 'Notebook'],
                            ]
        
        product_links = []                  
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData).find('td', {'class':'tableBox_output_td main'})
            
            try:
                nameCells = baseSoup.findAll('td', {'class': 'name name2_padd'})
            except:
                continue
            priceSpans = baseSoup.findAll('span', {'class': 'productSpecialPrice'})
            
            for i in range(len(nameCells)):
                nameLink = nameCells[i].find('a')
                priceSpan = priceSpans[i]

                url = nameLink['href'].split('&osCsid')[0]
                product_links.append([url, ptype])

        return product_links


