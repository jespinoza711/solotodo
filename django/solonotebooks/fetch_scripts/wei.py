import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
import re

class Wei(FetchStore):
    name = 'Wei'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, product_link):
        br = mechanize.Browser()
        data = br.open(product_link).get_data()
        soup = BeautifulSoup(data)
        
        availabilities = soup.find('table', { 'class' : 'pdisponibilidad' }).findAll('td')
        
        for availability in availabilities:
            if len(availability.contents) > 1 and 'Producto agotado' in availability.contents[1]:
                return None
        
        productData = ProductData()

        title = soup.find('title').string.split(
            'WEI CHILE - ')[1].encode('ascii', 'ignore')

        price = int(soup.find('table', { 'class' : 'pprecio' }).find('h1').string.replace('&nbsp;', '').strip().replace('.', ''))
        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = product_link
        productData.comparison_field = productData.url

        return productData


    # Main method
    def retrieve_product_links(self):
        base_url = 'http://www.wei.cl/'
        browser = mechanize.Browser()

        category_urls = [
            ['1261', 'Notebook'],      # Notebooks
            ['1306', 'VideoCard'],     # Tarjetas de video NVIDIA
            ['1307', 'VideoCard'],     # Tarjetas de video AMD
            ['1312', 'VideoCard'],     # Tarjetas de video AGP
            ['1117', 'Processor'],     # Procesadores
            ['1248', 'Screen'],    # LCD TV
            ['1245', 'Screen'],     # Monitores LCD
            ['1126', 'Motherboard'],     # MB
            ['1239', 'Ram'],     # RAM PC
            ['1241', 'Ram'],     # RAM Notebook
            ['511', 'StorageDrive'],     # HDD PC SATA
            ['512', 'StorageDrive'],     # HDD PC IDE
            ['513', 'StorageDrive'],     # HDD Notebook SATA
            ['514', 'StorageDrive'],     # HDD Notebook IDE
            ['515', 'StorageDrive'],     # SSD
            ['1222', 'PowerSupply'],     # Fuentes de poder
            ['1220', 'ComputerCase'],     # Gabinetes c/ PSU
            ['1221', 'ComputerCase'],     # Gabinetes s/ PSU
        ]

        link_pattern = r'ir\(\'(.+)\'\);$'

        product_links = {}
        for category_url, ptype in category_urls:
            desde = 1

            while True:
                page_url = base_url + 'index.htm?op=categoria&ccode=' +\
                      category_url + '&desde=' + str(desde)

                soup = BeautifulSoup(browser.open(page_url).get_data())

                product_cells = soup.findAll('div', 'box1')
                flag = False

                if not product_cells:
                    break

                for cell in product_cells:
                    url = re.match(link_pattern, cell['onclick']).groups()[0]
                    if url in product_links:
                        flag = True
                        break
                    product_links[url] = ptype

                if flag:
                    break

                desde += 20

        return product_links.items()
