#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore
import json

class LaPolar(FetchStore):
    name = 'La Polar'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        try:
            product_name = product_soup.find('div', { 'class': 'LetraDetalleProducto' }).string.encode('ascii', 'ignore')
        except AttributeError:
            return None
        
        product_price = int(product_soup.findAll('span', { 'class': 'PrecioDetalleRojo' })[1].string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.lapolar.cl'
        urlBuscarProductos = '/internet/catalogo/listados/'
        urlExtensions = [
                            ['electronica/computacion/notebook/', 'Notebook'], 
                            ['electronica/computacion/netbook/', 'Notebook'],
                            ['electrohogar/tv_video/led/', 'Screen'],
                            ['electrohogar/tv_video/lcd/', 'Screen'],
                            ]
       
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        for urlExtension, ptype in urlExtensions:
            page = 1;
            while(True):
                urlWebpage = urlBase + urlBuscarProductos + urlExtension + str(page)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)
                
                try:
                    raw_json_data = json.loads(baseSoup.findAll('script')[-3].string.strip().replace('var listado_productos_json = ', '')[:-1])
                except ValueError:
                    break
                
                json_product_array_data = []
                
                for row in raw_json_data['lista_completa']:
                    json_product_array_data.extend(row['sub_lista'])

                for json_product_data in json_product_array_data:
                    product_id = json_product_data['prid']
                    
                    url = 'http://www.lapolar.cl/internet/catalogo/detalles/%s%s' % (urlExtension, product_id)
                    
                    products_data.append([url, ptype])
                    
                page += 1

        return products_data

