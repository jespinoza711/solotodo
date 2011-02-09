import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import date
import mechanize
import re
import htmlentitydefs
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element

def get_average_score(id_vga, id_test):
    base_url = 'http://3dmark.com/search?resultTypeId=' + id_test + '&linkedDisplayAdapters=1&cpuModelId=0&chipsetId=' + id_vga + '&page='
    
    page_number = 0
    scores = []
    while True:
        url = base_url + str(page_number)
        print url
        browser = mechanize.Browser()
        data = browser.open(url).get_data()
        soup = BeautifulSoup(data)
        
        score_divs = soup.findAll('div', { 'class': 'span-2 label result-table-score' })
        if not score_divs:
            break
            
        scores.extend([int(div.string.replace('P', '')) for div in score_divs])
        
        page_number += 1
        
    if not scores:
        print 0
    
    return sum(scores) / len(scores)

def main():
    id_vga = sys.argv[1]
    id_test = '192'
    
    score = get_average_score(id_vga, id_test)
    print score

if __name__ == '__main__':
    main()
