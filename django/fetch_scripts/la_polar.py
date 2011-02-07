#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class LaPolar:
    name = 'La Polar'
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_name = product_soup.find('div', { 'class': 'LetraDetalleProducto' }).string.encode('ascii', 'ignore')
        product_price = int(product_soup.find('div', { 'id': 'fichaPrecioNormal' }).find('span').string.split('$')[1].split('pesos')[0].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        print product_data
        return product_data


    # Main method
    def get_products(self):
        print 'Getting La Polar notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.lapolar.cl'
        urlBuscarProductos = '/internet/catalogo/listados/'
        urlExtensions = [
                            'tecnologia/computacion/notebook/', 
                            'tecnologia/computacion/netbook/',
                            'electrohogar/refrigeracion/refrigerador_conv_1p']
       
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        product_links = []
        products_data = []
        for urlExtension in urlExtensions:
            page = 1;
            while(True):
                urlWebpage = urlBase + urlBuscarProductos + urlExtension + str(page)

                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                # Obtain the links to the other pages of the catalog (2, 3, ...)
                productRows = baseSoup.find("td", { "colspan" : "3" })
                
                if not productRows:
                    break
                
                productRows = productRows.find("table").findAll("tr", recursive = False)[1::2]
                
                if len(productRows) == 0:
                    break

                for productRow in productRows:
                    productCells = productRow.findAll("td", recursive = False)[::2]
                    for productCell in productCells:
                        titleField = productCell.find("div", {'class': 'letraNormalBold'})
                        link = titleField.find("a")['href']
                        product_links.append(link)
                page = page + 1
                
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product) 

        return products_data

