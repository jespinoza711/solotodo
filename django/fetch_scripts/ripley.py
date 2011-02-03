#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Ripley:
    name = 'Ripley'

    # Main method
    def getNotebooks(self):
        print 'Getting Ripley notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.ripley.cl'
        urlBuscarProductos = '/webapp/wcs/stores/servlet/categoria-TVRipley-10051-001772-130000-ESP-N--?curPg='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        productUrls = []
        comparisonFields = []
        j = 1                    
        while True:
            urlWebpage = urlBase + urlBuscarProductos + str(j)
            print urlWebpage

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productParagraphs = baseSoup.findAll("td", { "class" : "grisCatalogo" })
            productParagraphs = productParagraphs[1::3]
            productParagraphs = productParagraphs[:len(productParagraphs)/2]
            productParagraphs = [pp.parent.parent for pp in productParagraphs]
            
            if not productParagraphs:
                break
                
            for p in productParagraphs:
                names = p.findAll('td', {'class': 'grisCatalogo'})
                #print len(names)
                #print names[1]
                names = names[1].find('p').contents
                name = names[0].strip() + ' ' + names[2].strip()
                name = name.strip().replace('&nbsp;', '')
                #print name
                try:
                    price = p.find('span', {'class': 'normalHOME'}).string
                    price = int(price.replace('$', '').replace('.', ''))    
                except:
                    price = p.find('div', {'class': 'rojo'}).find('strong').contents[0]
                    price = int(price.replace('$', '').replace('.', ''))            
                            
                #print price
                url = 'http://www.ripley.cl/webapp/wcs/stores/servlet/' + p.find('a')['href']
                #print url
                if url in productUrls:
                    return productsData
                
                pd = ProductData()
                pd.custom_name = name
                pd.url = url
                pd.price = price
                pd.comparison_field = url
                productUrls.append(url)
                print pd
                productsData.append(pd)
                
            j += 1
            
        return productsData
