import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

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
            if 'Producto agotado' in availability.contents[1]:
                return None
        
        productData = ProductData()

        title = soup.find('title').string.split('WEI CHILE S. A. - ')[1]


        price = int(soup.find('table', { 'class' : 'pprecio' }).find('h1').string.replace('&nbsp;', '').strip().replace('.', ''))
        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = product_link
        productData.comparison_field = productData.url

        return productData


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlStore = 'http://www.wei.cl/'
        urlBase = urlStore + 'index.htm?op=categoria&ccode='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        product_links = []
        links = []
        
        category_urls = [
            ['252', 'Notebook'],      # Notebooks
            ['175', 'VideoCard'],     # Tarjetas de video AGP
            ['176', 'VideoCard'],     # Tarjetas de video PCI Express
            ['119', 'Processor'],     # Procesadores AMD
            ['120', 'Processor'],     # Procesadores Intel
            ['205', 'Screen'],    # LCD TV
            ['80', 'Screen'],     # Monitores LCD
            ['65', 'Motherboard'],     # MB AMD
            ['84', 'Motherboard'],     # MB Intel
            ['68', 'Ram'],     # RAM Notebook
            ['89', 'Ram'],     # RAM DDR
            ['195', 'Ram'],     # RAM DDR2
            ['199', 'Ram'],     # RAM DDR3
            ['70', 'StorageDrive'],     # HDD IDE
            ['71', 'StorageDrive'],     # HDD SATA
            ['78', 'StorageDrive'],     # HDD Notebook
            ['9', 'PowerSupply'],     # Fuentes de poder
        ]
                     
        
        for category_url, ptype in category_urls:
            desde = 1
            while True:
                urlWebpage = urlBase + category_url + '&desde=' + str(desde)
                
                # Obtain and parse HTML information of the base webpage
                baseData = browser.open(urlWebpage).get_data()
                baseSoup = BeautifulSoup(baseData)

                product_cells = baseSoup.findAll('div', { 'class': 'box1'})
                flag = False
                
                if not product_cells:
                    break
                    
                for cell in product_cells:
                    link = urlStore + cell.parent['href']
                    if link in links:
                        flag = True
                        break
                    product_links.append([link, ptype])
                    links.append(link)
                
                if flag:
                    break
                    
                desde += 20

        return product_links


