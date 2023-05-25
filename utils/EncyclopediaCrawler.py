import requests
from bs4 import BeautifulSoup
import scrapy
import re

class SearchDisplayItems(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    info = scrapy.Field()

def SearchDisplay(url):
    item_list = []
    page_list = []
    # Make the HTTP request to the website
    response = requests.get(url)
    response.encoding = 'utf-8'
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <fieldset> elements with class="roundBox"
    fieldsets = soup.find_all('fieldset', class_='roundBox')[1].find_all('td')[1:][::3]
    if fieldsets == []:
        return [],[]
    for element in fieldsets[:-1]:
        element_url = 'https://www.botanyvn.com/'+'%20'.join(element.find('a')['href'].strip().split())
        name_info = re.findall(r'>(.*?)<', str(element))
        name_info = [x.strip() for x in name_info if x]
        item = SearchDisplayItems()
        item['url'] = element_url
        try:
            item['name'] = name_info[0]
        except:
            item['name'] = ''
        try:
            item['type'] = name_info[1]
        except:
            item['type'] = ''
        try:
            item['info'] = name_info[2]
        except:
            item['info'] = ''
        item_list.append(item)

    for element in fieldsets[-1].find_all('a'):
        page_list.append(element['href'])

    return item_list,page_list

def SearchItem(url):
    # Make the HTTP request to the website
    response = requests.get(url)
    response.encoding = 'utf-8'
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <fieldset> elements with class="roundBox"
    fieldsets = soup.find_all('fieldset', class_='roundBox')[:2]
    try:
        info = fieldsets[0].find('p').get_text()
        info = re.sub(r'(Tên tiếng Anh:)', r'\n\1', info)
        info = re.sub(r'(Tên tiếng Việt:)', r'\n\1', info)
        info = re.sub(r'(Tên khác:)', r'\n\1', info)
    except:
        info = ''
    try:
        descryption = '\n'.join([a.get_text() for a in fieldsets[1].find_all('p')])
    except:
        descryption = ''

    return info, descryption


#items, pages = SearchDisplay('https://www.botanyvn.com/cnt.asp?param=edir&q=chim%20te&t=comname')
#info, descryption = SearchItem('https://www.botanyvn.com/cnt.asp?param=edir&v=Acanthophippium%20striatum&list=species')