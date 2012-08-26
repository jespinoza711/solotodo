import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from utils import clean_price_string

class SamsungStore(FetchStore):
    name = 'Samsung Store'
    use_existing_links = False

    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        soup = BeautifulSoup(browser.open(product_link).get_data())

        title = soup.find('h1').string.encode('ascii', 'ignore')

        price_string = soup.findAll('span', 'price')[-1].string
        price = int(clean_price_string(price_string))

        productData = ProductData()
        productData.custom_name = title
        productData.price = price
        productData.url = product_link
        productData.comparison_field = productData.url

        return productData

    def retrieve_product_links(self):
        browser = mechanize.Browser()

        url_extensions = [
            ['computacion-1/notebook.html', 'Notebook'],
            ['computacion-1/netbook.html', 'Notebook'],
            ['computacion-1/monitores/monitor.html', 'Screen'],
            ['computacion-1/monitores/monitor-tv-1.html', 'Screen'],
            ['tv-audio-video-1/televisores.html', 'Screen'],
        ]

        product_urls_and_types = {}

        for url_extension, product_type in url_extensions:
            page_number = 1

            while True:
                url_webpage = 'http://www.samsungstore.cl/%s?p=%d' % (url_extension, page_number)

                base_data = browser.open(url_webpage).get_data()
                soup = BeautifulSoup(base_data)

                link_containers = soup.findAll('li', 'item')

                if not link_containers:
                    break

                break_flag = False

                for link_container in link_containers:
                    url = link_container.find('a')['href']
                    if url in product_urls_and_types:
                        break_flag = True
                        break
                    product_urls_and_types[url] = product_type

                if break_flag:
                    break

                page_number += 1

        return product_urls_and_types.items()
