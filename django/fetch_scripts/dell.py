#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Dell:
    name = 'Dell'

    # Method that extracts the data of a specific product given its page
    def retrieveHomeProductsData(self, productUrl, productName, urlBase):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productsData = []
        
        dataDivs = soup.findAll("div", { "class" : "cg_alignNs" })
        numNtbks = len(dataDivs) / 2
        
        for i in range(numNtbks):
            productData = ProductData()
            urlDiv = dataDivs[i]
            linkTag = urlDiv.find('a')
            url = linkTag['href']
            if url[0] == '/':
                url = urlBase + url
            
            productData.url = url
            productData.custom_name = productName + ' ' + url
            
            priceDiv = dataDivs[numNtbks + i]
            priceTag = priceDiv.find('span', {'class': 'pricing_retail_nodiscount_price'})
            productData.price = int(priceTag.string.replace('CLP$', '').replace('.', ''))
            productsData.append(productData)

        return productsData      
        
    def retrieveVostroProductsData(self, productUrl, productName, urlBase):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        productsData = []
        
        dataDivs = soup.findAll("div", { "class" : "cg_alignNs" })
        numNtbks = len(dataDivs) / 2
        realDataDivs = soup.findAll("div", { "class" : "cg_align" })
        
        for i in range(numNtbks):
            productData = ProductData()
            urlDiv = realDataDivs[i]
            linkTag = urlDiv.find('a')
            if not linkTag:
                urlDiv = realDataDivs[numNtbks + i]
                linkTag = urlDiv.find('a')
            url = linkTag['href']
            if url[0] == '/':
                url = urlBase + url
            
            productData.url = url
            productData.custom_name = productName + ' ' + url
            
            data = br.open(url).get_data()
            soup = BeautifulSoup(data)
            priceTag = soup.find('span', {'class': 'pricing_retail_nodiscount_price'})         

            productData.price = int(priceTag.string.replace('CLP$', '').replace('.', ''))
            productsData.append(productData)

        return productsData         
        
    def retrieveAlienwareProductData(self, productUrl, productName):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        cotizadorLink = soup.findAll("a", { "class" : "lnk" })[2]['href']
        data = br.open(cotizadorLink).get_data()
        soup = BeautifulSoup(data)

        productData = ProductData()
        productData.url = productUrl
        productData.custom_name = productName

        priceTag = soup.find('span', {'class': 'pricing_retail_nodiscount_price'})
        productData.price = int(priceTag.string.replace('CLP$', '').replace('.', ''))
        return productData

    # Main method
    def getNotebooks(self):
        print 'Getting Dell notebooks'
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www1.la.dell.com'
        urlBuscarProductos = '/cl/es/'
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        
        url_extensions = [  'domesticos/Notebooks/inspnnb-mini/ct.aspx?refid=inspnnb-mini&s=dhs&cs=cldhs1',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll("table", { "width" : "728" })
            modelNavigator = modelNavigator[len(modelNavigator) - 1]
            modelNavigator = modelNavigator.findAll('tr')[2]
            homeModelsCells = modelNavigator.findAll('td')[:-2]
            
            modelUrls = []
            modelNames = []
            for modelCell in homeModelsCells:
                modelLinks = modelCell.findAll('a')
                for modelLink in modelLinks:
                    modelUrls.append(urlBase + modelLink['href'])
                    modelNames.append(modelLink.string)
            
            productsData = []
            for i in range(len(modelUrls)):
                productsData += self.retrieveHomeProductsData(modelUrls[i], modelNames[i], urlBase)
                
            alienwareModelsCells = modelNavigator.findAll('td')[-2]
            modelUrls = []
            modelNames = []
            for modelCell in alienwareModelsCells:
                modelLinks = modelCell.findAll('a')
                for modelLink in modelLinks:
                    modelUrls.append(urlBase + modelLink['href'])
                    modelNames.append(modelLink.string)

            for i in range(len(modelUrls)):
                productsData.append(self.retrieveAlienwareProductData(modelUrls[i], modelNames[i]))
        
        # Now for the business (Vostro / Latitude / Precision)        
        url_extensions = [  'empresas/notebooks/ct.aspx?refid=notebooks&s=bsd&cs=clbsdt1&~ck=mn',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll("table", { "width" : "688" })
            modelNavigator = modelNavigator[len(modelNavigator) - 1]
            categoryLinks = modelNavigator.findAll('a', {'class': 'lnk'})
            vostroLink = urlBase + categoryLinks[0]['href']
            
            data = browser.open(vostroLink).get_data()
            soup = BeautifulSoup(data)
            
            vostroCells = soup.findAll('div', {'class': 'para'})
            
            for vostroCell in vostroCells:
                vostroName = vostroCell.find('b').string
                vostroLink = urlBase + vostroCell.parent.find('a')['href']
                #productsData += self.retrieveVostroProductsData(vostroLink, vostroName, urlBase)
            
            latitudeLink = urlBase + categoryLinks[1]['href']
        
            data = browser.open(latitudeLink).get_data()
            soup = BeautifulSoup(data)
            
            latitudeCells = soup.findAll('div', {'class': 'para'})
            
            for latitudeCell in latitudeCells:
                productData = ProductData()
                productData.custom_name = latitudeCell.find('b').string
                productData.url = urlBase + latitudeCell.parent.find('a')['href']
                productData.price = int(latitudeCell.parent.find('span', {'class': 'pricing_retail_nodiscount_price'}).string.replace('CLP$', '').replace('.', ''))
                productsData.append(productData)

            precisionLink = urlBase + categoryLinks[2]['href']
        
            data = browser.open(precisionLink).get_data()
            soup = BeautifulSoup(data)
            
            precisionCells = soup.findAll('div', {'class': 'para'})[1:]
            numNtbks = len(precisionCells) / 3
            linkCells = soup.find('table', { 'width': '688' })
            linkCells = linkCells.findAll('a')
            priceCells = soup.findAll('span', { 'class': 'pricing_retail_nodiscount_price' })
            
            for i in range(numNtbks):
                productData = ProductData()
                productData.custom_name = precisionCells[i].find('b').string
                productData.url = urlBase + linkCells[2*i]['href']
                productData.price = int(priceCells[i].string.replace('CLP$', '').replace('.', ''))
                productsData.append(productData)                
                
        for productData in productsData:
            print productData
            
        return productsData

