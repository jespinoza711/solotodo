#!/usr/bin/env python

import mechanize
from mechanize import HTTPError
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace('&quot;', '"')
    s = s.replace('&apos;', "'")
    s = s.replace("&amp;", "&")
    return s

class AbcDin(FetchStore):
    name = 'AbcDin'
    use_existing_links = False
    
    def retrieve_product_data(self, product_link):
        try:
            product_webpage = mechanize.urlopen(product_link)
        except HTTPError:
            return None

        product_soup = BeautifulSoup(product_webpage.read())

        try:
            product_name = product_soup.find('h1', {'id': 'catalog_link'}).string
        except AttributeError:
            return None
        product_name = product_name.strip().encode('ascii', 'ignore')

        # Product not available check
        if product_soup.find('span', 'button_bottom'):
            return None

        product_price = product_soup.find('span', {'id': 'offerPrice'}).string
        product_price = int(clean_price_string(product_price))

        product_data = ProductData()
        product_data.custom_name = product_name
        product_data.url = product_link
        product_data.price = product_price
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        ajax_resources = [
            ['11620', 'Notebook'],
            ['11619', 'Notebook'],
            ['11607', 'Television'],
        ]

        product_links = []

        for category_id, ptype in ajax_resources:
            url = 'http://www.abcdin.cl/webapp/wcs/stores/servlet/'\
                  'AjaxCatalogSearchResultView?searchTermScope=&'\
                  'searchType=1000&filterTerm=&orderBy=&maxPrice=&'\
                  'showResultsPage=true&langId=-5&beginIndex=0&'\
                  'sType=SimpleSearch&metaData=&pageSize=1000&'\
                  'manufacturer=&resultCatEntryType=&catalogId='\
                  '10001&pageView=image&searchTerm=&minPrice=&'\
                  'categoryId={0}&storeId=10001'.format(category_id)
            base_data = mechanize.urlopen(url)
            base_soup = BeautifulSoup(base_data.read())

            for ntbk_data in base_soup.findAll('td', 'item'):
                url = ntbk_data.find('a')['href']
                product_links.append([url, ptype])

        return product_links