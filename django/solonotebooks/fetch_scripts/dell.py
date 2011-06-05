#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore

class Dell(FetchStore):
    name = 'Dell'
    urlBase = 'http://www.dell.com'
    use_existing_links = False
    
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)
        
        try:
            title = soup.find('div', { 'id': 'scpcc_title' }).find('img')['alt'].encode('ascii', 'ignore')
        except:
            return None
        price = int(soup.find(['tr', 'td'], { 'class': 'pricing_dotdotdot' }).findAll('span')[-1].string.split('$')[1].replace('.', ''))
        
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url
        return productData
        
    def retrieve_subline_links(self, url):
        mecha = mechanize.urlopen(url)
        soup = BeautifulSoup(mecha.read())
        
        buttons = soup.findAll('div', {'class': 'buttons'})
        links = [button.find('a')['href'] for button in buttons]
        
        if not links:
            redirected_url = mecha.geturl()
            if 'configure' in redirected_url:
                final_links = [[redirected_url, 'Notebook']]
            else:
                final_links = []
        else:
            final_links = [[link, 'Notebook'] for link in links if 'configure' in link]
            
        return final_links
        
    def retrieve_line_links(self, url):
        r = mechanize.urlopen(url)
        soup = BeautifulSoup(r.read())
        
        sub_line_containers = soup.findAll('div', {'class': 'infoCol'})
        sub_line_urls = [container.find('a')['href'] for container in sub_line_containers]
        fixed_urls = [self.urlBase + url[:-2] + 'fs' for url in sub_line_urls]
        
        links = []
        for url in fixed_urls:
            links.extend(self.retrieve_subline_links(url))
            
        return links

    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MyProgram/0.1)'),
                 ('From', 'responsible.person@example.com')]
        mechanize.install_opener(opener)
        
        urlBuscarProductos = '/cl/'
        product_links = []
        
        
        # Start home
        url_extensions = [  
            'p/laptops?avt=series&avtsub=inspiron-mini-netbooks&~ck=supertab-inspiron-mini-netbooks',
                         ]
                            
        for url_extension in url_extensions:
            urlWebpage = self.urlBase + urlBuscarProductos + url_extension
            
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            tab_navigator = baseSoup.find('div', {'class': 'superTabarellaTabContainer'})
            line_urls = [self.urlBase + link['href'] for link in tab_navigator.findAll('a')]

            for url in line_urls:
                product_links.extend(self.retrieve_line_links(url))
        
        # Start business
        
        url_extensions = [  
            'empresas/p/laptops.aspx',
                         ]
                            
        for url_extension in url_extensions:
            urlWebpage = self.urlBase + urlBuscarProductos + url_extension
            r = mechanize.urlopen(urlWebpage)
            baseSoup = BeautifulSoup(r.read())

            line_title_containers = baseSoup.findAll('div', { 'class' : 'productTitle' })
            line_urls = [self.urlBase + div.find('a')['href'] for div in line_title_containers if div.find('a')]
            for url in line_urls:
                product_links.extend(self.retrieve_line_links(url))
        
        # Start Screen
        
        url_extensions = [  
            '/content/products/compare.aspx/19_22widescreen?c=cl&cs=cldhs1&l=es&s=dhs',
            '/content/products/compare.aspx/23_30widescreen?c=cl&cs=cldhs1&l=es&s=dhs',
            '/cl/es/empresas/Monitores/19_15widescreen/cp.aspx?refid=19_15widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/22_20widescreen/cp.aspx?refid=22_20widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/30_24widescreen/cp.aspx?refid=30_24widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/20_19flatpanel/cp.aspx?refid=20_19flatpanel&s=bsd&cs=clbsdt1',
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
            for link in links:
                if 'configure' in link['href']:
                    product_links.append([link['href'], 'Screen'])
            
        return product_links

