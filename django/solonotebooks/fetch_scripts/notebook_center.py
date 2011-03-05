#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class NotebookCenter(FetchStore):
    name = 'NotebookCenter'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_subnames = [unicode(str(subpart), errors = 'ignore').strip() for subpart in product_soup.find('td', { 'class': 'menus3' }).findAll('div')[-1].contents]
        
        product_name = ' '.join(product_subnames).strip()
        
        product_price = int(product_soup.find('td', { 'width': '258' }).find('div').findAll('div')[1].contents[0].split('$')[1].split('IVA')[0].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.notebookcenter.cl/'
        urlBuscarProductos = 'centrodetalle.php'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  '?id_categoria=308', # Macbook Air
                            '?id_categoria=307', # Macbook Pro
                            '?id_categoria=403', # Netbook HP
                            '?id_categoria=404', # Netbook Lenovo
                            '?id_categoria=405', # Netbook Packard Bell
                            '?id_categoria=406', # Netbook Samsung
                            '?id_categoria=429', # Netbook Sony
                            '?id_categoria=440', # Netbook Viewsonic
                            '?id_categoria=61',  # Notebook Acer
                            '?id_categoria=251', # Notebook Dell
                            '?id_categoria=505', # Notebook Gamer
                            '?id_categoria=57',  # Notebook HP
                            '?id_categoria=64',  # Notebook Lenovo
                            '?id_categoria=342', # Notebook MSI
                            '?id_categoria=58',  # Notebook Packard Bell
                            '?id_categoria=418', # Notebook Samsung
                            '?id_categoria=212', # Notebook Sony
                            '?id_categoria=63',  # Notebook Toshiba
                            '?id_categoria=534', # Notebook Viewsonic
                            '?id_categoria=275', # Monitores Apple
                            '?id_categoria=162', # Monitores LCD
                            ]
                          
        product_links = []  
        for url_extension in url_extensions:
            index = 1
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&indice=' + str(index)

                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                rawNames = baseSoup.findAll("span", { "class" : "subtit2" })[1::2]
                
                if not rawNames:
                    break
                    
                rawLinks = baseSoup.findAll("a", { "target" : "ifrm_centro" })
                
                for rawLink in rawLinks:
                    link = urlBase + rawLink['href']
                    link = link.split('&id_categoria')[0]
                    product_links.append(link)

                index += 1

        return product_links
