import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Wei:
    name = 'Wei'

    # Method that extracts the data of a specific product given its page
    def retrieveProductData(self, productUrl):
	    br = mechanize.Browser()
	    data = br.open(productUrl).get_data()
	    soup = BeautifulSoup(data)

	    productData = ProductData()

	    titleSpans = soup.findAll("div", { "class" : "TXTSM" })
	    title = titleSpans[0].string.strip()

	    priceCells = soup.findAll("td", { "class" : "TXTB" })
	    price = int(priceCells[1].string.strip().replace(',', ''))
	    productData.custom_name = title
	    productData.price = price
	    productData.url = productUrl
	    productData.comparison_field = productData.url
	    
	    print productData

	    return productData


    # Main method
    def getNotebooks(self):
        print 'Getting Wei notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.wei.cl'
        urlBuscarProductos = '/catalogue/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
                            
        urlWebpage = urlBase + urlBuscarProductos + 'category.htm?action=subcategory&ccode=NB&sccode=79#sub'

        # Obtain and parse HTML information of the base webpage
        print urlWebpage
        baseData = browser.open(urlWebpage).get_data()
        baseSoup = BeautifulSoup(baseData)

        # Obtain the links to the other pages of the catalog (2, 3, ...)
        productLinks = baseSoup.findAll("a", { "class" : "TXTSMNU" })
        productLinks = productLinks[:-10]
        
        for productLink in productLinks:
            productsData.append(self.retrieveProductData(productLink['href']))

        return productsData

