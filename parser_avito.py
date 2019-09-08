import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import codecs
from random import choice, uniform
from time import sleep
from lxml.html import fromstring
from itertools import cycle
import traceback

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

useragents = open('useragents.txt').read().split('\n')
#proxies = open('proxies.txt').read().split('\n')

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

#proxies = get_proxies()
#proxy_pool = cycle(proxies)

def get_html(url):
    sleep(uniform(2, 5))
    response = requests.get(url) #, headers=useragent, proxies={'https': 'http://' + proxy}
    #print(response.json())
    return response.text
    '''for i in range(1,11):
        #Get a proxy from the pool
        proxy = next(proxy_pool)
        print(i)
        useragent = {'User-Agent': choice(useragents)}
        try:'''
        #uniform(2, 5)

        #except:
        #    print("Skipping. Connnection error")


def get_proxy_and_useragent(url):
    proxy = {'http': 'http://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}
    while True:
        #uniform(2, 5)
        sleep(1)
        proxy = {'http': 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(useragents)}
        try:
            html = get_html(url, useragent, proxy)
            soup = BeautifulSoup(html, 'lxml')
            if re.search('Доступ временно заблокирован', soup.text)==None:
                break
        except:
            continue
    return (proxy, useragent)

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('apartments.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['rooms'],
                         data['square'],
                         data['living_space'],
                         data['kitchen_area'],
                         data['cur_floor'],
                         data['max_floor'],
                         data['home_type'],
                         data['price'],
                         data['payment_method'],
                         data['district'],
                         data['street']))


def get_page_data(html):
    print('start')
    soup = BeautifulSoup(html, 'lxml')
    try:
        divs = soup.find('div', class_='js-catalog-list')
    except:
        print('error')
        exit
    ads = divs.find_all('div', class_='item_table')
    for ad in ads:
        try:
            div = ad.find('div', class_='description').find('h3')
            url = 'https://www.avito.ru' + div.find('a')['href']
            title = div.text.strip().split(', ')
            rooms = title[0][0]
            if (rooms == 'С'):
                rooms = 0
            square = float(title[1].split(' ')[0])
            floors = re.match(r'(\d+)/(\d+)', title[2]).groups(0)
            cur_floor = floors[0]
            max_floor = floors[1]
        except:
            rooms = -1
            square = 0
            cur_floors = -1
            max_floor = -1
        try:
            tmp_price = ad.find('div', class_='about').find('span', class_='price').text.strip().split('₽')
            price = int(re.sub(' ', '', tmp_price[0].strip()))
            payment_method = tmp_price[1].strip()
            if payment_method == '':
                payment_method = 'once'
        except:
            price = ''
            payment_method = ''
        try:
            address = ad.find('div', class_='').find('p', class_ = 'address').text.strip()
            district = address.split(', ')[0]
            street = address.replace(address.split(', ')[0] + ', ', '').replace('Ростов-на-Дону,', '')
        except:
            address = ''
            street = ''
        try:
            #proxy, useragent = get_proxy_and_useragent(url)
            html_tmp = get_html(url)
            soup_tmp = BeautifulSoup(html_tmp, 'lxml')
            divs_tmp = soup_tmp.find('div', class_ = 'item-view-main').find('ul', class_ = 'item-params-list').find_all('li')
            home_type = ''
            living_space = ''
            kitchen_area = ''
            for div_tmp in divs_tmp:
                if re.search('Тип дома', div_tmp.text) != None:
                    home_type = div_tmp.text.split(':')[1].strip()
                elif re.search('Жилая площадь', div_tmp.text) != None:
                    living_space = re.sub('м²', '', div_tmp.text.split(':')[1]).strip()
                elif re.search('Площадь кухни', div_tmp.text) != None:
                    kitchen_area = re.sub('м²', '', div_tmp.text.split(':')[1]).strip()
        except:
            home_type = ''
            living_space = ''
            kitchen_area = ''
        data = {'rooms':rooms,
                'square':square,
                'living_space': living_space,
                'kitchen_area': kitchen_area,
                'cur_floor':cur_floor,
                'max_floor':max_floor,
                'home_type': home_type,
                'price':price,
                'payment_method': payment_method,
                'district': district,
                'street':street}
        print('finish')
        write_csv(data)


def main():
   # url = "https://www.avito.ru/rostov-na-donu/kvartiry?p=1"
    base_url = 'https://www.avito.ru/rostov-na-donu/kvartiry?p='
    with open('apartments.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('rooms',
                         'square, м²',
                         'living_space, м²',
                         'kitchen_area, м²',
                         'cur_floor',
                         'max_floor',
                         'home_type',
                         'price, RUB',
                         'payment_method',
                         'district',
                         'street'))
    for i in range(1, 11):
        url_gen = base_url + str(i)
        #proxy, useragent = get_proxy_and_useragent(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()
