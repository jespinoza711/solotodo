#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class HPOnline(FetchStore):
    name = 'HP Online'
    use_existing_links = False
    
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
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.hponline.cl'
        urlBuscarProductos = '/personas/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['productos.aspx?cmd=Z2w=', 'Notebook'],
                            ['productos.aspx?cmd=ZWw=', 'Notebook'],
                            ['remates.aspx', 'Notebook'],
                            ]
                          
        product_links = []                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            ntbkCells = baseSoup.findAll('div', { 'class' : 'grid_item' })
            
            for ntbkCell in ntbkCells:
                product_links.append([urlBase + urlBuscarProductos + ntbkCell.find('a')['href'], ptype])
                
        return product_links
