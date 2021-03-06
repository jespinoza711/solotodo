#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class ENotebook(FetchStore):
    name = 'E-Notebook'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        product_data = browser.open(product_link).get_data()
        product_soup = BeautifulSoup(product_data)
        
        product_cells = product_soup.findAll('td', { 'class': 'pageHeading' })
        
        try:
            product_name = product_cells[0].find('h1').contents[0]
        except IndexError:
            return None
        price_cell = product_cells[1]
        
        try:
            product_price = int(price_cell.find('span', { 'class' : 'productSpecialPrice' }).string.replace('$', '').replace('.', ''))
        except Exception:
            product_price = int(price_cell.string.split('$')[1].replace('.', ''))
        
        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data
    
    def extract_product_links(self, page_link):
        br = mechanize.Browser()
        data = br.open(page_link).get_data()
        soup = BeautifulSoup(data)
        product_links = []
        cellis = soup.findAll("td", { "class" : "productListing-data" })
        cells = cellis[1::4]
        for i in range(len(cells)):
            link = cells[i].find("a")
            product_links.append(link['href'].split('?osCsid')[0])
        return product_links

    # Method that extracts the products from a given catalog page
    def extract_product_pages(self, base_page_link):
        br = mechanize.Browser()
        data = br.open(base_page_link).get_data()
        soup = BeautifulSoup(data)
        links = [base_page_link]
        pageLinks = soup.findAll("a", { "class" : "pageResults" })[:-1]
        for pageLink in pageLinks:
            link = pageLink['href'].split('&osCsid')[0]
            links.append(link)
            
        return links

    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.notebook.cl/'
        urlBuscarProductos = 'venta/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        url_extensions = [
            ['it-index-n-notebooks-cP-1.html', 'Notebook'],
        ]
                        
        extra_pagelinks = [
            ['it-index-n-memoria_notebook-cP-46_4.html', 'Ram'],
            ['it-index-n-discos_duros-cP-46_23.html', 'StorageDrive'],
        ]
                        
        pageLinks = []
        for url_extension, ptype in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            table_navigator = baseSoup.findAll('table', { "cellpadding" : "2" })[1]
            
            pageNavigator = table_navigator.findAll("td", { "class" : "smallText" })
            for pn in pageNavigator:
                link = pn.find("a")
                try:
                    pageLinks.append([link['href'].split('?osCsid')[0], ptype])
                except Exception:
                    continue
        
        for page_link, ptype in extra_pagelinks:
            pageLinks.append([urlBase + urlBuscarProductos + page_link, ptype])
        
        product_link_pages = []
        for pageLink, ptype in pageLinks:
            links = self.extract_product_pages(pageLink)
            for link in links:
                product_link_pages.append([link, ptype])
            
        product_links = []
        for product_link_page, ptype in product_link_pages:
            for link in self.extract_product_links(product_link_page):
                product_links.append([link, ptype])
                
        return product_links

