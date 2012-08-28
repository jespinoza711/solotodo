#!/usr/bin/env python
import urllib2

import mechanize
from BeautifulSoup import BeautifulSoup
from . import ProductData, FetchStore
from solonotebooks.cotizador.utils import clean_price_string

class Dell(FetchStore):
    name = 'Dell'
    urlBase = 'http://www.dell.com'
    use_existing_links = False
    
    def retrieve_product_data(self, productUrl):
        br = mechanize.Browser()
        data = br.open(productUrl).get_data()
        soup = BeautifulSoup(data)

        try:
            title = soup.find('span', 'para_intropara').string
        except AttributeError:
            try:
                title = soup.find('div', {
                    'id': 'scpcc_title'}).find('img')['alt']
            except AttributeError:
                return None

        title = title.encode('ascii', 'ignore')

        price = soup.find(['tr', 'td'], {'class': 'pricing_dotdotdot'})
        price = price.findAll('span')[-1].string.split('$')[1]
        price = int(clean_price_string(price))

        prices = {}
        for p in ['credit_card', 'deposit', 'wire_transfer']:
            prices[p] = price
        productData = ProductData()

        productData.custom_name = title
        productData.price = price
        productData.url = productUrl
        productData.comparison_field = productData.url

        return productData

    def retrieve_product_links(self):
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (MyProgram/0.1)'),
            ('From', 'responsible.person@example.com')]
        mechanize.install_opener(opener)

        url_buscar_productos = '/cl/'
        product_links = []
        url_base = 'http://www.dell.com'

        # Start home
        url_extensions = [
            'p/laptops?cat=laptops',
            ]

        for url_extension in url_extensions:
            url_webpage = url_base + url_buscar_productos + url_extension

            r = mechanize.urlopen(url_webpage)
            soup = BeautifulSoup(r.read())

            notebook_lines_container = soup.find('div',
                'tabschegoryGroups')
            notebook_lines = notebook_lines_container.findAll('div',
                recursive=False)

            notebook_urls = []
            for line in notebook_lines:
                for container in line.findAll('div', 'prodImg'):
                    link = container.find('a')['href'].replace('pd', 'fs')
                    notebook_urls.append(url_base + link)

            for url in notebook_urls:
                for url in self.retrieve_line_links(url):
                    product_links.append([url, 'Notebook'])

        # Start business

        url_extensions = [
            'empresas/p/laptops',
            ]

        for url_extension in url_extensions:
            url_webpage = url_base + url_buscar_productos + url_extension
            r = mechanize.urlopen(url_webpage)
            soup = BeautifulSoup(r.read())

            product_containers = soup.findAll('div', 'carouselProduct')
            for container in product_containers:
                url = url_base + container.find('a')['href']
                for url in self.retrieve_enteprise_links(url):
                    product_links.append([url, 'Notebook'])

        # Start Monitor
        url_extensions = [
            '/content/products/compare.aspx/19_22widescreen'
            '?c=cl&cs=cldhs1&l=es&s=dhs',
            '/content/products/compare.aspx/23_30widescreen'
            '?c=cl&cs=cldhs1&l=es&s=dhs',
            '/cl/es/empresas/Monitores/19_15widescreen/cp.aspx'
            '?refid=19_15widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/22_20widescreen/cp.aspx'
            '?refid=22_20widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/30_24widescreen/cp.aspx'
            '?refid=30_24widescreen&s=bsd&cs=clbsdt1',
            '/cl/es/empresas/Monitores/20_19flatpanel/cp.aspx'
            '?refid=20_19flatpanel&s=bsd&cs=clbsdt1',
            ]

        for url_extension in url_extensions:
            url_webpage = url_base + url_extension

            r = mechanize.urlopen(url_webpage)
            soup = BeautifulSoup(r.read())

            links = soup.findAll('a', {'class': 'lnk'})
            for link in links:
                if 'configure' in link['href']:
                    product_links.append([link['href'], 'Screen'])

        return product_links

    def retrieve_enteprise_links(self, url):
        me = mechanize.urlopen(url)
        soup = BeautifulSoup(me.read())

        urls = []
        for link in soup.findAll('a', 'purchase'):
            url = link['href']
            if 'configure' in url:
                urls.append(url)

        return urls

    def retrieve_line_links(self, url):
        try:
            me = mechanize.urlopen(url)
        except urllib2.HTTPError:
            return []
        soup = BeautifulSoup(me.read())
        custom_config_containers = soup.findAll('div', 'buttons')

        real_url = me.geturl()

        if not custom_config_containers and 'configure' in real_url:
            return [real_url]

        links = []
        for container in custom_config_containers:
            links.append(container.find('a')['href'])

        return links