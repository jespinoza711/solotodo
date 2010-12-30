#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData
import pdb

class Dell:
    name = 'Dell'

    # Method that extracts the data of a specific product given its page
    def retrieveHomeProductsData(self, productUrl, productName, urlBase):
        r = mechanize.urlopen(productUrl)
        soup = BeautifulSoup(r.read())

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
                
            if 'configure' in url or 'upsell' in url:           
                productData.url = url
                productData.custom_name = productName
                
                priceDiv = dataDivs[numNtbks + i]
                priceTag = priceDiv.find('span', {'class': 'pricing_retail_nodiscount_price'})
                if not priceTag:
                    priceTag = priceDiv.find('span', {'class': 'pricing_sale_price'})
                if not priceTag:
                    continue 
                productData.price = int(priceTag.string.replace('CLP$', '').replace('.', ''))
                productData.comparison_field = productData.url
                productsData.append(productData)
            else:
                productsData += self.retrieveHomeProductsData(url, productName, urlBase)

        return productsData      
        
    def retrieveVostroProductsData(self, productUrl, productName, urlBase):
        r = mechanize.urlopen(productUrl)
        soup = BeautifulSoup(r.read())

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
            productData.comparison_field = productData.url	    
            
            r = mechanize.urlopen(url)
            soup = BeautifulSoup(r.read())
            priceTag = soup.find('span', {'class': 'pricing_retail_nodiscount_price'})
            if not priceTag:
                priceTag = soup.find('span', {'class': 'pricing_sale_price'})
            if not priceTag:
                continue    

            productData.price = int(round(float(priceTag.string.replace('CLP$', '').replace('.', '').replace(',', '.'))))
            productsData.append(productData)

        return productsData         
        
    def retrieveAlienwareProductData(self, productUrl, productName):
        r = mechanize.urlopen(productUrl)
        soup = BeautifulSoup(r.read())
        
        productsData = []

        cotizadorLinks = soup.findAll("a", { "class" : "lnk" })
        
        for cotizadorLink in cotizadorLinks:
            productUrl = cotizadorLink['href']
            if 'configure' not in productUrl:
                continue
               
            r = mechanize.urlopen(productUrl)
            soup = BeautifulSoup(r.read())

            productData = ProductData()
            productData.url = productUrl
            productData.custom_name = productName
            productData.comparison_field = productData.url	    

            priceTag = soup.find('span', {'class': 'pricing_retail_nodiscount_price'})
            if not priceTag:
                priceTag = soup.find('span', {'class': 'pricing_sale_price'})

            try:
                productData.price = int(priceTag.string.replace('CLP$', '').replace('.', ''))
            except:
                continue
            
            inList = False
            for pd in productsData:
                if productData.comparison_field == pd.comparison_field:
                    inList = True
                    break
            
            if not inList:
                productsData.append(productData)
                    
        return productsData

    # Main method
    def getNotebooks(self):
        print 'Getting Dell notebooks'
        
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; MyProgram/0.1)"),
                 ("From", "responsible.person@example.com")]
        mechanize.install_opener(opener)
        
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www1.la.dell.com'
        urlBuscarProductos = '/cl/es/'
        
        
        # Array containing the data for each product
        productsData = []
        
        
        url_extensions = [  'domesticos/Notebooks/inspnnb-mini/ct.aspx?refid=inspnnb-mini&s=dhs&cs=cldhs1',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll("td", { "style" : "width:300px;" })
            modelNavigator = modelNavigator[len(modelNavigator) / 2:]            
            homeNavigators = modelNavigator[:-2]
            
            modelUrls = []
            modelNames = []            
            
            for homeNavigator in homeNavigators:
                modelLinks = homeNavigator.findAll('a')
                for modelLink in modelLinks:
                    modelUrls.append(urlBase + modelLink['href'])
                    modelNames.append(modelLink.string)
            
            productsData = []
            for i in range(len(modelUrls)):
                productsData += self.retrieveHomeProductsData(modelUrls[i], modelNames[i], urlBase)
                pass
                
            alienwareModelLinks = modelNavigator[-2].findAll('a')
            modelUrls = []
            modelNames = []
            for alienwareModelLink in alienwareModelLinks:
                modelUrls.append(urlBase + alienwareModelLink['href'])
                modelNames.append(alienwareModelLink.string)

            for i in range(len(modelUrls)):
                productsData += self.retrieveAlienwareProductData(modelUrls[i], modelNames[i])
        
        # Now for the business (Vostro / Latitude / Precision)        
        url_extensions = [  'empresas/notebooks/ct.aspx?refid=notebooks&s=bsd&cs=clbsdt1&~ck=mn',
                            ]
                            
        for url_extension in url_extensions:
            urlWebpage = urlBase + urlBuscarProductos + url_extension
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll("table", { "width" : "688" })
            modelNavigator = modelNavigator[len(modelNavigator) - 1]
            categoryLinks = modelNavigator.findAll('a', {'class': 'lnk'})
            vostroLink = urlBase + categoryLinks[0]['href']
            
            r = mechanize.urlopen(vostroLink)
            soup = BeautifulSoup(r.read())
            
            vostroCells = soup.findAll('div', {'class': 'para'})
            
            for vostroCell in vostroCells:
                vostroName = vostroCell.find('b').string
                vostroLink = urlBase + vostroCell.parent.find('a')['href']
                productsData += self.retrieveVostroProductsData(vostroLink, vostroName, urlBase)
            
            latitudeLink = urlBase + categoryLinks[1]['href']
        
            r = mechanize.urlopen(latitudeLink)
            soup = BeautifulSoup(r.read())
            
            latitudeCells = soup.findAll('div', {'class': 'para'})
            
            for latitudeCell in latitudeCells:
                productData = ProductData()
                productData.custom_name = latitudeCell.find('b').string
                productData.url = urlBase + latitudeCell.parent.find('a')['href']
                span = latitudeCell.parent.find('span', {'class': 'pricing_retail_nodiscount_price'})
                if not span:
                    span = latitudeCell.parent.find('span', {'class': 'pricing_sale_price'})
                try:
                    productData.price = int(span.string.replace('CLP$', '').replace('.', ''))
                except:
                    continue
                productData.comparison_field = productData.url	    
                productsData.append(productData)

            precisionLink = urlBase + categoryLinks[2]['href']
        
            r = mechanize.urlopen(precisionLink)
            soup = BeautifulSoup(r.read())
            
            precisionCells = soup.findAll('div', {'class': 'para'})[1:]
            numNtbks = len(precisionCells) / 3
            linkCells = soup.find('table', { 'width': '688' })
            linkCells = linkCells.findAll('a')
            priceCells = soup.findAll('table', { 'width': '688' })
            priceCells = priceCells[len(priceCells) - 1]
            priceCells = priceCells.findAll('td', {'class': 'gridCell'})
            
            for i in range(numNtbks):
                productData = ProductData()
                productData.custom_name = precisionCells[i].find('b').string
                productData.url = urlBase + linkCells[2*i]['href']
                priceSpan = priceCells[i].find('span', {'class': 'pricing_retail_nodiscount_price'})
                if not priceSpan:
                    continue
                productData.price = int(priceSpan.string.replace('CLP$', '').replace('.', ''))
                productData.comparison_field = productData.url
                productsData.append(productData)  
                
        for productData in productsData:
            print productData
            
        return productsData

