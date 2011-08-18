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
        
        availabilities = soup.findAll("div", { "class" : "TXTSM" })[1].contents[2::4]
        
        for availability in availabilities:
            if 'agotado' in availability:
                return None

        productData = ProductData()

        titleSpans = soup.findAll("div", { "class" : "TXTSM" })
        title = titleSpans[0].string.strip()

        priceCells = soup.findAll('td', { 'class' : 'TXTRBIG' })
        price = int(priceCells[1].string.strip().replace(',', ''))
        productData.custom_name = title.encode('ascii','ignore')
        productData.price = price
        productData.url = product_link
        productData.comparison_field = productData.url

        return productData


    # Main method
    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.wei.cl/catalogue/category.htm?action=subcategory&ccode='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        product_links = []
        links = []
        
        category_urls = [
                    ['NB&sccode=79', 'Notebook'],      # Notebooks
                    ['TV&sccode=133', 'VideoCard'],     # Tarjetas de video AGP
                    ['TV&sccode=134', 'VideoCard'],     # Tarjetas de video PCI Express
                    ['CP&sccode=57', 'Processor'],     # Procesadores AMD
                    ['CP&sccode=58', 'Processor'],     # Procesadores Intel
                    ['MO&sccode=162', 'Screen'],    # LCD TV
                    ['MO&sccode=19', 'Screen'],     # Monitores LCD
                    ['MB&sccode=23', 'Motherboard'],     # MB AMD
                    ['MB&sccode=24', 'Motherboard'],     # MB Intel
                        ]
                            
        for category_url, ptype in category_urls:
            urlWebpage = urlBase + category_url
            
            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            try:
                productLinks = baseSoup.find('table', { 'cellpadding': '5'}).findAll("a", { "class" : "TXTSMNU" })
            except AttributeError, e:
                continue
                
            for link in productLinks:
                link = link['href']
                if link in links:
                    continue
                links.append(link)
                product_links.append([link, ptype])

        return product_links


