#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class HPOnline:
    name = 'HP Online'

    # Main method
    def getNotebooks(self):
        print 'Getting HP Online notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://hponline.techdata.cl'
        urlBuscarProductos = '/personas/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        url_extensions = [  'productos.aspx?cmd=Z2x4eA==',
                            'productos.aspx?cmd=ZWx4eA==',
                            'remates.aspx',
                            ]
                          
        pageLinks = []                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            print urlWebpage

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            ntbkCells = baseSoup.findAll('div', { 'class' : 'grid_item' })
            
            for ntbkCell in ntbkCells:
                productData = ProductData()
                link = urlBase + urlBuscarProductos + ntbkCell.find('a')['href']
                productData.url = link
                productData.comparison_field = link
                productData.custom_name = ntbkCell.find('span', { 'class' : 'grid_title' }).string
                productData.price = int(ntbkCell.findAll('div', { 'class' : 'grid_price' })[1].find('span').string.replace('Precio Oferta:', '').replace('$', '').replace('.', ''))
                print productData
                productsData.append(productData)
        return productsData
