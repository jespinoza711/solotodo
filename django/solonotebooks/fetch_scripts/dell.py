#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Dell(FetchStore):
    name = 'Dell'
    urlBase = 'http://www1.la.dell.com'
    use_existing_links = False
    
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)
        
        try:
            title = soup.find('div', { 'id': 'scpcc_title' }).find('img')['alt'].encode('ascii', 'ignore')
        except:
            title = soup.find('title').string
            if 'Sitio Oficial' in title:
                return None
            else:
                raise Exception('Error al indexar url ' + productUrl)
        price = int(soup.find(['tr', 'td'], { 'class': 'pricing_dotdotdot' }).findAll('span')[-1].string.split('$')[1].replace('.', ''))
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData
    
    def retrieve_configure_link(self, url):
        r = mechanize.urlopen(url)
        sub_soup = BeautifulSoup(r.read())
        links = sub_soup.findAll('a', { 'class': 'lnk' })
        for link in links:
            if 'configure' in link['href']:
                return link['href']

    # Method that extracts the data of a specific product given its page
    def retrieve_home_links(self, productUrl):
        r = mechanize.urlopen(productUrl)
        soup = BeautifulSoup(r.read())

        product_links = []
        
        dataDivs = soup.findAll('div', { 'class' : 'cg_alignNs' })
        numNtbks = len(dataDivs) / 2
        
        for i in range(numNtbks):
            urlDiv = dataDivs[i]
            linkTag = urlDiv.find('a')
            url = linkTag['href']
            if url[0] == '/':
                url = self.urlBase + url
                
            if 'configure' in url or 'upsell' in url:           
                priceDiv = dataDivs[numNtbks + i]
                priceTag = priceDiv.find('span', {'class': 'pricing_retail_nodiscount_price'})
                if not priceTag:
                    priceTag = priceDiv.find('span', {'class': 'pricing_sale_price'})
                if not priceTag:
                    continue 
                product_links.append(url)
            else:
                product_links.extend(self.retrieve_home_links(url))

        return product_links
        
    def retrieve_vostro_links(self, productUrl):
        r = mechanize.urlopen(productUrl)
        soup = BeautifulSoup(r.read())

        product_links = []
        
        dataDivs = soup.findAll('div', { 'class' : 'cg_alignNs' })
        numNtbks = len(dataDivs) / 2
        realDataDivs = soup.findAll('div', { 'class' : 'cg_align' })
        
        for i in range(numNtbks):
            urlDiv = realDataDivs[i]
            linkTag = urlDiv.find('a')
            if not linkTag:
                urlDiv = realDataDivs[numNtbks + i]
                linkTag = urlDiv.find('a')
            url = linkTag['href']
            if url[0] == '/':
                url = self.urlBase + url

            product_links.append(url)

        return product_links
        
    def retrieve_alienware_links(self, productUrl):
        try:
            r = mechanize.urlopen(productUrl)
        except:
            return []
        soup = BeautifulSoup(r.read())
        product_links = []
        cotizadorLinks = soup.findAll('a', { 'class' : 'lnk' })
        
        for cotizadorLink in cotizadorLinks:
            productUrl = cotizadorLink['href']
            if 'configure' not in productUrl:
                continue
               
            product_links.append(productUrl)
        return list(set(product_links))

    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MyProgram/0.1)'),
                 ('From', 'responsible.person@example.com')]
        mechanize.install_opener(opener)
        
        urlBuscarProductos = '/cl/es/'
        product_links = []
        
        url_extensions = [  
            'domesticos/Notebooks/inspnnb-mini/ct.aspx?refid=inspnnb-mini&s=dhs&cs=cldhs1',
                         ]
                            
        for url_extension in url_extensions:
            urlWebpage = self.urlBase + urlBuscarProductos + url_extension
            
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll('td', { 'style' : 'width:300px;' })
            modelNavigator = modelNavigator[len(modelNavigator) / 2:]            
            homeNavigators = modelNavigator[:-2]
            
            modelUrls = []
            modelNames = []            
            
            for homeNavigator in homeNavigators:
                modelLinks = homeNavigator.findAll('a')
                for modelLink in modelLinks:
                    modelUrls.append(self.urlBase + modelLink['href'])
                    modelNames.append(modelLink.string)
            
            for i in range(len(modelUrls)):
                product_links.extend(self.retrieve_home_links(modelUrls[i]))
                
            alienwareModelLinks = modelNavigator[-2].findAll('a')
            modelUrls = []
            modelNames = []
            for alienwareModelLink in alienwareModelLinks:
                modelUrls.append(self.urlBase + alienwareModelLink['href'])
                modelNames.append(alienwareModelLink.string)

            for i in range(len(modelUrls)):
                product_links.extend(self.retrieve_alienware_links(modelUrls[i]))
        
        # Now for the business (Vostro / Latitude / Precision)        
        url_extensions = [  
            'empresas/notebooks/ct.aspx?refid=notebooks&s=bsd&cs=clbsdt1&~ck=mn',
                         ]
                            
        for url_extension in url_extensions:
            urlWebpage = self.urlBase + urlBuscarProductos + url_extension
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            # Obtain the links to the other pages of the catalog (Inspiron 11z, Inspiron 14...)
            modelNavigator = baseSoup.findAll('table', { 'width' : '688' })
            modelNavigator = modelNavigator[len(modelNavigator) - 1]
            categoryLinks = modelNavigator.findAll('a', {'class': 'lnk'})
            vostroLink = self.urlBase + categoryLinks[0]['href']
            
            r = mechanize.urlopen(vostroLink)
            soup = BeautifulSoup(r.read())
            
            vostroCells = soup.findAll('div', {'class': 'para'})
            
            for vostroCell in vostroCells:
                vostroName = vostroCell.find('b').string
                vostroLink = self.urlBase + vostroCell.parent.find('a')['href']
                product_links.extend(self.retrieve_vostro_links(vostroLink))
            
            latitudeLink = self.urlBase + categoryLinks[1]['href']
        
            r = mechanize.urlopen(latitudeLink)
            soup = BeautifulSoup(r.read())
            
            latitudeCells = soup.findAll('div', {'class': 'para'})
            
            for latitudeCell in latitudeCells:
                url = latitudeCell.parent.find('a')['href']
                if 'dell.com' not in url:
                    url = self.urlBase + url
                    product_links.append(self.retrieve_configure_link(url))
                else:
                    product_links.append(url)

            precisionLink = self.urlBase + categoryLinks[2]['href']
            r = mechanize.urlopen(precisionLink)
            soup = BeautifulSoup(r.read())
            
            precisionCells = soup.findAll('div', {'class': 'para'})
            numNtbks = len(precisionCells) / 3
            linkCells = soup.find('table', { 'width': '688' })
            linkCells = linkCells.findAll('a')
            priceCells = soup.findAll('table', { 'width': '688' })
            priceCells = priceCells[len(priceCells) - 1]
            priceCells = priceCells.findAll('td', {'class': 'gridCell'})
            
            for i in range(numNtbks):
                url = self.urlBase + linkCells[2*i]['href']
                priceSpan = priceCells[i].find('span', {'class': 'pricing_retail_nodiscount_price'})
                if not priceSpan:
                    continue
                product_links.append(self.retrieve_configure_link(url))
        
        # Monitores        
        url_extensions = [  
            '/content/products/compare.aspx/19_22widescreen?c=cl&cs=cldhs1&l=es&s=dhs',
            '/content/products/compare.aspx/23_30widescreen?c=cl&cs=cldhs1&l=es&s=dhs',
                         ]
                            
        for url_extension in url_extensions:
            urlWebpage = self.urlBase + url_extension
            
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())
            
            prices = baseSoup.findAll('span', {'class': ['pricing_sale_price', 'pricing_retail_nodiscount_price']})
            prices = [int(price.contents[0].replace('CLP$', '').replace('.', '')) for price in prices]
            num_prods = len(prices)
            names = baseSoup.findAll('span', {'class': 'title_emph'})[3:num_prods + 3]
            names = [name.contents[0] for name in names]
            links = baseSoup.findAll('a', {'class': 'lnk'})
            final_links = []
            for link in links:
                if 'configure' in link['href']:
                    final_links.append(link['href'])
            product_links.extend(final_links[:num_prods])
            
        return product_links

