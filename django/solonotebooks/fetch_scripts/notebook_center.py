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
        
        product_name = ' '.join(product_subnames).strip().replace('<br />', '')
        
        product_price = int(product_soup.find('td', { 'width': '258' }).find('div').contents[2].split('$')[1].split('IVA')[0].replace('.', ''))
        
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
        urlBuscarProductos = 'centrodetalle.php?id_categoria='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['308', 'Notebook'],  # Macbook Air
                            ['307', 'Notebook'],  # Macbook Pro
                            ['403', 'Notebook'],  # Netbook HP
                            ['404', 'Notebook'],  # Netbook Lenovo
                            ['405', 'Notebook'],  # Netbook Packard Bell
                            ['406', 'Notebook'],  # Netbook Samsung
                            ['429', 'Notebook'],  # Netbook Sony
                            ['440', 'Notebook'],  # Netbook Viewsonic
                            ['61', 'Notebook'],   # Notebook Acer
                            ['251', 'Notebook'],  # Notebook Dell
                            ['505', 'Notebook'],  # Notebook Gamer
                            ['57', 'Notebook'],   # Notebook HP
                            ['64', 'Notebook'],   # Notebook Lenovo
                            ['342', 'Notebook'],  # Notebook MSI
                            ['58', 'Notebook'],   # Notebook Packard Bell
                            ['418', 'Notebook'],  # Notebook Samsung
                            ['212', 'Notebook'],  # Notebook Sony
                            ['63', 'Notebook'],   # Notebook Toshiba
                            ['534', 'Notebook'],  # Notebook Viewsonic
                            ['275', 'Screen'],  # Monitores Apple
                            ['162', 'Screen'],  # Monitores LCD
                            ]
                          
        product_links = []  
        for url_extension, ptype in url_extensions:
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
                    product_links.append([link, ptype])

                index += 1

        return product_links
