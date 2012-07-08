#!/usr/bin/env python
import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore

class Lider(FetchStore):
    name = 'Lider'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        name = soup.find('h3').string.encode('ascii', 'ignore')

        internet_price = int(soup.find('p', 'precio').find('em').string.replace('$', '').replace('.', ''))

        productData = ProductData()
        productData.custom_name = name
        productData.price = internet_price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData

    # Main method
    def retrieve_product_links(self):
        url_base = 'http://www.lider.cl/dys/catalog/product/productList.jsp?'

        # Browser initialization
        browser = mechanize.Browser()

        url_extensions = [
            ['id=CAT_GM_00164&cId=CAT_GM_00755&pId=CAT_GM_00140&navAction=jump&navCount=2', 'Notebook'],
            ['id=CAT_GM_00162&cId=CAT_GM_00755&pId=CAT_GM_00140&navAction=jump&navCount=16', 'Notebook'],
            ['id=CAT_GM_00178&cId=CAT_GM_00682&pId=CAT_GM_00140&navAction=jump&navCount=2', 'Screen'],
            ['id=CAT_GM_00175&cId=CAT_GM_00172&pId=CAT_GM_00096&navAction=jump&navCount=2', 'Screen'],
            ['id=CAT_GM_00176&cId=CAT_GM_00172&pId=CAT_GM_00096&navAction=jump&navCount=2', 'Screen'],
        ]

        product_urls = {}

        for url_extension, ptype in url_extensions:
            page_number = 1

            while True:
                url = url_base + url_extension + '&goToPage=' +\
                      str(page_number)

                soup = BeautifulSoup(browser.open(url).get_data())

                product_ul = soup.find('ul', 'products')

                if not product_ul:
                    break

                product_lis = product_ul.findAll('li', 'product')

                for p in product_lis:
                    product_url = p.find('a')['href']
                    product_urls['http://www.lider.cl' + product_url] = ptype

                page_number += 1

        return product_urls.items()

