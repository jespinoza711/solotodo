#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Eprod(FetchStore):
    name = 'Eprod'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        stock_status = soup.find('div', {'id': 'vmMainPage'}).find('span', { 'class': 'productPrice' })
        
        if not stock_status:
            return None

        productData = ProductData()

        title = soup.find("title").string.strip()
        
        price = int(soup.find('div', {'id': 'vmMainPage'}).find('span', { 'class': 'productPrice' }).string.strip().replace('$', '').replace(',', ''))

        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.eprod.cl'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        
        url_extensions = [
            ['?category_id=1', 'Notebook'],     # Notebooks
            ['?category_id=3', 'Notebook'],     # Netbooks
            ['?category_id=26', 'Screen'],      # Pantallas
            ['?category_id=40', 'Ram'],         # RAM
        ]
        
        productLinks = []
        links = []
        
        for url_extension, ptype in url_extensions:
            
            urlWebpage = urlBase + '/' + url_extension + '&page=shop.browse&limit=100'

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            rawLinks = baseSoup.find('div', {'id': 'vmMainPage'}).findAll("h3", { "class" : "browseProductTitle" })
            
            for rawLink in rawLinks:
                link = rawLink.find("a")['href']
                if not link in links:
                    links.append(urlBase+link)
                    productLinks.append([urlBase+link, ptype])

        return productLinks

