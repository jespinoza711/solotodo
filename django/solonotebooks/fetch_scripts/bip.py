#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Bip(FetchStore):
    name = 'Bip'
    use_existing_links = False

    # Method that extracts the <a> tags to products given the URL of the catalog page
    def extract_links(self, pageUrl):
        br = mechanize.Browser()
        data = br.open(pageUrl).get_data()
        soup = BeautifulSoup(data)
        links = soup.findAll("a", { "class" : "menuprod" })[::2]

        return links

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()
        
        stock_info = soup.find('td', { 'class' : 'disp' })
        
        if not stock_info:
            return None
        
        stock_string = ''.join(str(stock) for stock in stock_info.contents)
        
        if 'Agotado' in stock_string:
            return None

        titleSpan = soup.find("td", { "class" : "menuprodg" })
        title = titleSpan.contents[0].strip()

        priceCell = soup.findAll("td", { "class" : "prc8" })
        price = int(str(priceCell[0].string).replace('.', '').replace('$', '').strip())

        productData.custom_name = title.encode('ascii','ignore').strip()
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url	    

        return productData

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.bip.cl/ecommerce/'
        urlBuscarProductos = 'index.php?modulo=busca&'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['categoria=191', 'Notebook'],                      # Netbooks
                            ['categoria=166', 'Notebook'],                      # Notebooks
                            ['categoria=118&categoria_papa=97', 'VideoCard'],   # Tarjetas de video
                            ['categoria=99&categoria_papa=111', 'Processor'],   # Proces Intel 775
                            ['categoria=339&categoria_papa=111', 'Processor'],  # Proces Intel 1155
                            ['categoria=262&categoria_papa=111', 'Processor'],  # Proces Intel 1156
                            ['categoria=263&categoria_papa=111', 'Processor'],  # Proces Intel 1366
                            ['categoria=100&categoria_papa=111', 'Processor'],  # Proces AMD AM2
                            ['categoria=242&categoria_papa=111', 'Processor'],  # Proces AMD AM3
                            ['categoria=19', 'Screen'],                         # LCD
                            ['categoria=108', 'Motherboard'],                   # Placas madre
                            ]
                            
        product_links = []
                            
        for url_extension, ptype in url_extensions:
            page_number = 0
            
            while True:
                urlWebpage = urlBase + urlBuscarProductos + url_extension + '&pagina=' + str(page_number)
                
                rawLinks = self.extract_links(urlWebpage)
                if not rawLinks:
                    break
                for rawLink in rawLinks:
                    product_links.append([urlBase + rawLink['href'], ptype])
                
                page_number += 1
                
        return product_links
