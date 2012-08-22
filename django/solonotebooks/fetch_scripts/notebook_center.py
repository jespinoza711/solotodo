#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class NotebookCenter(FetchStore):
    name = 'NotebookCenter'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)

        product_name = product_soup.find('span', {'class': 'titulo_producto'}).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('span', { 'class': 'precio_producto_efectivo' }).string.replace('$', '').replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        urlBase = 'http://www.notebookcenter.cl/'
        urlBuscarProductos = '?p=1&op=2&p3='
        browser = mechanize.Browser()
        
        url_extensions = [
            ['565', 'Notebook'],  # Macbook Air
            ['558', 'Notebook'],  # Macbook Pro
            ['61', 'Notebook'],   # Notebook Acer
            ['251', 'Notebook'],  # Notebook Dell
            ['57', 'Notebook'],   # Notebook HP
            ['64', 'Notebook'],   # Notebook Lenovo
            ['418', 'Notebook'],  # Netbook Samsung
            ['212', 'Notebook'],  # Notebook Sony
            ['63', 'Notebook'],   # Notebook Toshiba
            ['603', 'Notebook'],   # Notebook Corporativo Acer
            ['602', 'Notebook'],   # Notebook Corporativo Lenovo
            ['598', 'Notebook'],   # Notebook Corporativo HP
            ['606', 'Notebook'],   # Notebook Corporativo Dell
            ['401', 'Notebook'],  # Netbook Acer
            ['402', 'Notebook'],  # Netbook Dell
            ['406', 'Notebook'],  # Netbook Samsung
            ['472', 'Processor'],  # Procesadores AMD
            ['473', 'Processor'],  # Procesadores Intel
            ['275', 'Screen'],  # Monitores Apple
            ['162', 'Screen'],  # Monitores LCD
            ['640', 'Screen'],  # Monitores LED
            ['323', 'Screen'],  # Televisor LCD
            ['641', 'Screen'],  # Televisor LED
            ['6', 'Ram'],  # Notebook RAM
            ['109', 'StorageDrive'],  # HDD Notebook
            ['412', 'StorageDrive'],  # HDD Desktop
        ]
                          
        product_links = []  
        for url_extension, ptype in url_extensions:
            index = 0
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&i_p=' + str(index)
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)
                    
                product_containers = baseSoup.findAll("div", { "id" : "producto_inicio_inicio3" })
                if not product_containers:
                    break

                for product_container in product_containers:
                    js_data = product_container.find('a')['href']

                    js_arguments = [int(s) for s in js_data.replace("'", ' ').split() if s.isdigit()]
                    id_prod = js_arguments[4]
                    link = urlBase + '?p=2&op=1&i_p=' + str(id_prod)
                    product_links.append([link, ptype])

                index += 1

        return product_links
