#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Cintegral:
    name = 'Cintegral'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()

        titleSpan = soup.find("h1")
        title = str(titleSpan.string).strip()
        try:
            priceCell = soup.find("div", { "id" : "product-info" }).find("ul").findAll("li")[1].contents[1]
            price = int(str(priceCell.replace('.', '').replace('$', '')))
        except:
            priceCell = soup.find("div", { "id" : "product-info" }).find("ul").findAll("li")[2].contents[1]
            price = int(str(priceCell.replace('.', '').replace('$', '')))

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url

        return productData


    # Main method
    def get_products(self):
        print 'Getting Cintegral notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.cintegral.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        final_links = []
        
        url_extensions = [  'index.php?op=cat&id=84',
                            'index.php?op=cat&id=9'
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            links = baseSoup.findAll('a', { 'class' : 'style4' })
            prices = baseSoup.findAll('a', { 'class' : 'style5' })
            
            for i in range(len(links)):
                link = 'http://www.cintegral.cl/index.php' + links[i]['href']
                if link in final_links:
                    continue
                final_links.append(link)
                name = links[i].string.strip()
                price = int(prices[i].string.replace('$', '').replace('.', ''))
                product_data = ProductData()
                product_data.custom_name = name
                product_data.url = link
                product_data.comparison_field = link
                product_data.price = price
                print product_data
                productsData.append(product_data)

        return productsData

