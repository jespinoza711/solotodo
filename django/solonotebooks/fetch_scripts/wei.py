import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from utils import clean_price_string

class Wei(FetchStore):
    name = 'Wei'
    use_existing_links = False

    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, product_link):
        br = mechanize.Browser()
        soup = BeautifulSoup(br.open(product_link).get_data())

        name = soup.find('title').string.split(
            'WEI CHILE - ')[1].encode('ascii', 'ignore')

        not_available_image = soup.find('img', {
            'src': 'img/iconos/stocks/stk6.png'})

        if not_available_image:
            return name, {}


        price = soup.find('h2', 'precio').string
        price = int(clean_price_string(price))

        productData = ProductData()

        productData.custom_name = name
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
            ['1248', 'Television'],    # LCD TV
            ['1245', 'Monitor'],     # Monitores LCD
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

        product_links = {}
        for category_url, ptype in category_urls:
            desde = 1

            while True:
                page_url = base_url + 'index.htm?op=categoria&ccode=' +\
                           category_url + '&desde=' + str(desde)

                soup = BeautifulSoup(browser.open(page_url).get_data())

                product_cells = soup.findAll('div', 'producto_icono')
                flag = False

                if not product_cells:
                    break

                for cell in product_cells:
                    url = cell.find('a')['href']
                    if url in product_links:
                        flag = True
                        break
                    product_links[url] = ptype

                if flag:
                    break

                desde += 20

        return product_links.items()
