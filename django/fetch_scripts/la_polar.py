#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class LaPolar:
    name = 'La Polar'

    # Main method
    def getNotebooks(self):
        print 'Getting La Polar notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.lapolar.cl'
        urlBuscarProductos = '/internet/catalogo/listados/tecnologia/computacion/'
        urlExtensions = ['notebook/', 'netbook/']
       
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
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
                        name = titleField.find("a").string
                        link = titleField.find("a")['href']
                        priceField = productCell.find("div", {'class' : 'LetraPrecioDestacados'})
                        priceString = priceField.contents[0].replace('$', '').replace('.', '')
                        price = int(priceString)
                        productData = ProductData()
                        productData.custom_name = name
                        productData.url = link
                        productData.price = price
                        productData.comparison_field = productData.url
                        print productData
                        productsData.append(productData)
                page = page + 1

        return productsData

