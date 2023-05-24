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
    # Make the HTTP request to the website
    response = requests.get(url)
    response.encoding = 'utf-8'
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <fieldset> elements with class="roundBox"
    fieldsets = soup.find_all('fieldset', class_='roundBox')[1].find_all('td')[1:][::3]
    print(fieldsets)
    for element in fieldsets[:-1]:
        url = element.find('a')['href']
        name_info = re.findall(r'>(.*?)<', str(element))
        name_info = [x.strip() for x in name_info if x]
        item = SearchDisplayItems()
        item['name'] = name_info[0]
        item['type'] = name_info[1]
        try:
            item['info'] = name_info[2]
        except:
            item['info'] = ''
        item_list.append(item)

    return item_list