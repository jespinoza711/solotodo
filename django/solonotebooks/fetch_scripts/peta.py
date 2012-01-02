#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Peta(FetchStore):
    name = 'Peta'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link, already_tried = False):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except Exception:
            if already_tried:
                return None
            else:
                return self.retrieve_product_data(product_link, already_tried = True)
        product_soup = BeautifulSoup(product_data)
        
        try:
            product_availability = product_soup.find('p', { 'class': 'availability in-stock' }).find('span')
            if product_availability.string and product_availability.string != 'En existencia':
                return None
        except Exception:
            return None
        
        try:
            product_name = product_soup.find('h1', { 'class': 'p-title' }).string.encode('ascii', 'ignore')
            product_price = int(product_soup.find('span', { 'class': 'price' }).string.split('$')[1].replace('.', ''))
        except Exception:
            return None
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.peta.cl/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [  ['computadores-1/netbooks.html', 'Notebook'],
                            ['computadores-1/notebooks.html', 'Notebook'],
                            ['computadores-1/apple.html?appletype=898,903', 'Notebook'],
                            ['peta-cl/tarjetas-de-video.html', 'VideoCard'],
                            ['peta-cl/procesadores.html', 'Processor'],
                            ['peta-cl/monitores.html', 'Screen'],
                            ['audio-y-video-1/televisores.html', 'Screen'],
                            ['peta-cl/placas-madre-1.html', 'Motherboard'],
                            ['partes-y-piezas/memorias.html', 'Ram'],
                            ]
                          
        product_links = []
        links = []                            
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + url_extension
            pageNumber = 1
                
            while True:
                completeWebpage = urlWebpage + '?limit=36&p=' + str(pageNumber)

                baseData = browser.open(completeWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                baseSoup = baseSoup.find('div', 'category-products')
                ntbkCells = []
                ntbkCells.extend(baseSoup.findAll('li', { 'class': 'item first'}))
                ntbkCells.extend(baseSoup.findAll('li', { 'class': 'item'}))
                ntbkCells.extend(baseSoup.findAll('li', { 'class': 'item last'}))

                if not ntbkCells:
                    break

                trigger = False
                for ntbkCell in ntbkCells:
                    link = ntbkCell.find('a')['href']
                        
                    if link in links:
                        trigger = True
                        break
                        
                    links.append(link)
                    product_links.append([link, ptype])
                    
                if trigger:
                    break
                    
                pageNumber += 1

        return product_links

