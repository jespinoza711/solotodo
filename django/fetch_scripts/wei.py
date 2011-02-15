import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Wei:
    name = 'Wei'


    # Method that extracts the data of a specific product given its page
    def retrieve_product_data(self, product_link):
        br = mechanize.Browser()
        data = br.open(product_link).get_data()
        soup = BeautifulSoup(data)
        
        availabilities = soup.findAll("div", { "class" : "TXTSM" })[1].contents[2::4]
        
        for availability in availabilities:
            if 'agotado' in availability:
                return None

        productData = ProductData()

        titleSpans = soup.findAll("div", { "class" : "TXTSM" })
        title = titleSpans[0].string.strip()

        priceCells = soup.findAll("td", { "class" : "TXTB" })
        price = int(priceCells[1].string.strip().replace(',', ''))
        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = product_link
        productData.comparison_field = productData.url

        print productData

        return productData


    # Main method
    def get_products(self):
        print 'Getting Wei notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.wei.cl/catalogue/category.htm?action=subcategory&ccode='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        products_data = []
        product_links = []
        
        category_urls = [
                    'NB&sccode=79',      # Notebooks
                    'TV&sccode=133',     # Tarjetas de video AGP
                    'TV&sccode=134',     # Tarjetas de video PCI Express
                        ]
                            
        for category_url in category_urls:
            urlWebpage = urlBase + category_url

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            productLinks = baseSoup.find('table', { 'cellpadding': '5'}).findAll("a", { "class" : "TXTSMNU" })
            product_links.extend([link['href'] for link in productLinks])

        product_links = list(set(product_links))
        for product_link in product_links:
            product = self.retrieve_product_data(product_link)
            if product:
                products_data.append(product)                

        return products_data


