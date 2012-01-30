#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Webco(FetchStore):
    name = 'Webco'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('h1').contents[0].encode('ascii', 'ignore')
        product_price = int(product_soup.findAll('h2')[1].string.replace('.', '').replace('$', '').replace('cash', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www1.webco.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [
            # Netbooks
            ['n_new_productos.asp?CATEGORIA={761FD739-2D0F-4177-8AE0-C641D6F16502}', 'Notebook'],
            # Notebooks
            ['n_new_productos.asp?CATEGORIA={D70BBB30-F5E9-4246-B812-A939C8777429}', 'Notebook'],
            # Tarjetas de video
            ['n_new_productos.asp?CATEGORIA={FFE74755-6E24-4958-A066-F75670943D3E}', 'VideoCard'],
            # Procesadores AMD
            ['n_new_productos.asp?CATEGORIA={AA5D5535-B127-4AEE-8583-4529F66DE4D7}#ct_39', 'Processor'],
            # Procesadores Intel
            ['n_new_productos.asp?CATEGORIA={5701C20F-03E6-430E-8CCF-01EE820BEDF8}#ct_39', 'Processor'],
            # LCD TV
            ['n_new_productos.asp?CATEGORIA={E49A199E-214A-4658-99AA-7E6220434D8D}#ct_32', 'Screen'],
            # LCD
            ['n_new_productos.asp?CATEGORIA={79A1AF72-4B4D-4368-9205-FC0D646A1145}#ct_32', 'Screen'],
            # MB AMD
            ['n_new_productos.asp?CATEGORIA={C29A8E9A-5B73-4BEC-B6D7-665BA1B0D087}#ct_38', 'Motherboard'],
            # MB Intel
            ['n_new_productos.asp?CATEGORIA={9892E74D-67CD-4443-86F7-6FEBE141596B}#ct_38', 'Motherboard'],
            # HDD Notebook
            ['n_new_productos.asp?CATEGORIA={BCFA52D6-A416-4C48-BA90-F490B4F2C651}#ct_421', 'StorageDrive'],
            # HDD Notebook
            ['n_new_productos.asp?CATEGORIA={BCFA52D6-A416-4C48-BA90-F490B4F2C651}#ct_421', 'StorageDrive'],
            # HDD SATA
            ['n_new_productos.asp?CATEGORIA={80024ADB-0B06-4281-8CB6-7649D9E2C29B}#ct_421', 'StorageDrive'],
            # HDD IDE
            ['n_new_productos.asp?CATEGORIA={518AE532-05F0-4FEB-9FBE-3E67CA383E91}#ct_421', 'StorageDrive'],
            # RAM Desktop
            ['n_new_productos.asp?CATEGORIA={CB3ACADF-536F-4513-BD91-41E5E210B742}#ct_31', 'Ram'],
            # RAM Notebook
            ['n_new_productos.asp?CATEGORIA={B77F75B2-F280-4385-892A-01109D48ABD3}#ct_31', 'Ram'],
        ]
        
        product_links = []                    
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            productImages = baseSoup.findAll("img", { "width" : "193" })
            
            for productImage in productImages:
                productData = ProductData()
                try:
                    product_links.append([urlBase + productImage.parent['href'], ptype])
                except:
                    continue

        return product_links


