#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class HPOnline:
    name = 'HP Online'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('span', { 'id': 'ctl00_templateContenido_detalle1_iuNombre' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('div', { 'id': 'ctl00_templateContenido_detalle1_iuPanelML' }).string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data

    # Main method
    def get_products(self):
        print 'Getting HP Online notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://hponline.techdata.cl'
        urlBuscarProductos = '/personas/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        
        url_extensions = [  'productos.aspx?cmd=Z2x4eA==',
                            'productos.aspx?cmd=ZWx4eA==',
                            'remates.aspx',
                            ]
                          
        product_links = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            ntbkCells = baseSoup.findAll('div', { 'class' : 'grid_item' })
            
            for ntbkCell in ntbkCells:
                product_links.append(urlBase + urlBuscarProductos + ntbkCell.find('a')['href'])
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

                
        return products_data
