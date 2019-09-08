from bs4 import BeautifulSoup
import numpy as np
#from random import uniform
#from time import sleep
import csv
import re
#import time
from TorCrawler import TorCrawler

crawler = TorCrawler(ctrl_pass='mypassword')

def write_csv(data):
    with open('apartments_cian.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['rooms'],
                         data['square'],
                         data['living_space'],
                         data['kitchen_space'],
                         data['curr_floor'],
                         data['max_floor'],
                         data['home_type'],
                         data['build_year'],
                         data['district'],
                         data['serv_lift'],
                         data['pass_lift'],
                         data['parking'],
                         data['loggia'],
                         data['balcony'],
                         data['garbage_chute'],
                         data['bathroom'],
                         data['repair_type'],
                         data['wind_view'],
                         data['emergency_exit'],
                         data['avg_price_for_m'],
                         data['avg_room_price'],
                         data['price']))

def past_data_page(url):
    #soup = BeautifulSoup(html, 'lxml')
    try:
        soup = crawler.get(url)
        divs = soup.find('div', class_ = '_93444fe79c-wrapper--1Z8Nz')
        ads = divs.find_all('div', class_ = "_93444fe79c-card--2Jgih")
    except:
        return False
    i = 0
    while i < len(ads):
        print ('   Advertising %i start   ' % i)
        try:
            try:
             tmp_url = ads[i].find('div', class_='c6e8ba5398-info-section--28o47 c6e8ba5398-main-info--Rfnfh').find('a')['href']
            except:
             tmp_url = ads[i].find('div', class_ = 'undefined c6e8ba5398-main-info--Rfnfh').find('a')['href']
            #html = get_html(tmp_url)
            #tmp_soup = BeautifulSoup(html, 'lxml')
            tmp_soup = crawler.get(tmp_url)
            print('tmp_soup done')
        except:
            print('!!!!! %i TMP error !!!!!!' % i)
            crawler.rotate()
            continue
        district = np.nan
        try:
            d = tmp_soup.find('div', class_ = 'a10a3f92e9--header-information--38LX9').text
            district = re.search('р-н [А-Я][а-я]*', d).group(0).split()[1]
        except:
            pass
        price = np.nan
        try:
            tmp = tmp_soup.find('div', class_ = 'a10a3f92e9--container--CKANo').find('span', class_ = 'a10a3f92e9--price_value--1iPpd').find('span').text
            print('price done')
            price = float(re.sub('[(\xa0) ]', '', tmp)[:-1])

        except:
            print('!!!!! %i Price error !!!!!!' % i)
            crawler.rotate()
            continue
        try:
            block = tmp_soup.find('div', class_ = 'a10a3f92e9--info-block--3hCay').find_all('div', class_ = 'a10a3f92e9--info--2ywQI' )
            print('block done')
        except:
            print('block error')
            pass
        square = np.nan
        living_space = np.nan
        kitchen_scace = np.nan
        curr_floor = np.nan
        max_floor = np.nan
        #is_built = np.nan
        build_year = np.nan
        #build_quarter = np.nan
        try:
         if re.match('([а-я]+)(.*)', block[-1].text.lower()).group(1) == 'срок' and re.search('2019', block[-1].text) != None:
             i+=1
             continue
         for elem in block:
                r = re.match('([а-я]+)(.*)', elem.text.lower())
                if r.group(1) == 'общая':
                    square = float(r.group(2).split()[0].replace(',', '.'))
                elif r.group(1) == 'жилая':
                    living_space = float(r.group(2).split()[0].replace(',', '.'))
                elif r.group(1) == 'кухня':
                    kitchen_scace = float(r.group(2).split()[0].replace(',', '.'))
                elif r.group(1) == 'этаж':
                    tmp = r.group(2).split()
                    curr_floor = int(tmp[0])
                    max_floor = int(tmp[2])
                elif r.group(1) == 'построен':
                    #is_built = 1
                    build_year = int(r.group(2))
                    #build_quarter = 0
                # elif r.group(1) == 'срок':
                #     tmp = re.sub('[а-я\.]', '', r.group(2)).strip().split()
                #     is_built = 0
                #     build_year = tmp[1]
                #     build_quarter = tmp[0]
        except:
            pass
        try:
            gen_info = tmp_soup.find_all('div', class_ = 'a10a3f92e9--offer_card_page-main--1glTM')[1]
        except:
            pass

        serv_lift = 0
        pass_lift = 0
        parking = 0
        loggia = 0
        balcony = 0
        garbage_chute = 0
        try:
            lst = gen_info.find('ul', 'a10a3f92e9--container--L-EIV').find_all('li')
            for l in lst:
                l = l.text.lower().strip()
                if l == 'грузовой лифт':
                    serv_lift = 1
                elif l == 'пассажирский лифт':
                    pass_lift = 1
                elif l == 'паркинг':
                    parking = 1
                elif l == 'лоджия':
                    loggia = 1
                elif l == 'балкон':
                    balcony = 1
                elif l == 'мусоропровод':
                    garbage_chute = 1
        except:
            pass

        rooms = 0
        home_type = np.nan
        bathroom = np.nan
        repair_type = np.nan
        wind_view = np.nan

        try:
            lst = gen_info.find('section', class_ = 'a10a3f92e9--container--1MHfF').find('ul').find_all('li')
            for l in lst:
                l = re.match('([А-Я]([а-я]*\s*)*)(\d+|(\w+\s*)*)', l.text)
                if re.search('комнат', l.group(1).lower()):
                    rooms = int(l.group(3))
                elif  re.search('дома', l.group(1).lower()):
                    home_type = l.group(3)
                elif re.search('санузел', l.group(1).lower()):
                    bathroom = int(l.group(3))
                elif l.group(1).lower() == 'ремонт':
                    repair_type = l.group(3)
                elif re.search('вид', l.group(1).lower()):
                    wind_view = l.group(3)
        except:
            pass
        emergency_exit = np.nan
        try:
            lst =  tmp_soup.find('div', class_ = 'a10a3f92e9--container--3dDSQ').find_all('div', class_ = 'a10a3f92e9--column--2oGBs')[1].find_all('div', class_ = 'a10a3f92e9--item--2Ig2y')
            for l in lst:
                l = re.match('([А-Я]([а-я]*\s*)*)(\d+|(\w+\s*)*)', l.text)
                if l.group(1).lower() == 'аварийный':
                    if l.group(3) == 'нет':
                        emergency_exit = 0
                    else:
                        emergency_exit = 1
        except:
            pass

        avg_price_for_m = np.nan

        try:
            columns = tmp_soup.find('div', class_ = 'a10a3f92e9--container--2uCrP').find_all('div', class_ = 'a10a3f92e9--column--2j52r')
        except:
            pass

        try:
            lst = columns[0].find_all('div', class_ = 'a10a3f92e9--item--1oGyE')
            for l in lst:
                if re.search('средняя цена', l.text.lower()):
                    avg_price_for_m = float(re.sub('[^0-9,]', '', l.text))
        except:
            pass

        avg_room_price = np.nan
        try:
            lst = columns[1].find_all('div', class_ = 'a10a3f92e9--item--1oGyE')
            for l in lst:
                if re.search('средняя цена', l.text.lower()):
                    avg_room_price = float(re.sub('[^0-9,]', '', l.text)[1:].replace(',', ''))
        except:
            pass

        data = {'rooms': rooms,
                'square': square,
                'living_space': living_space,
                'kitchen_space': kitchen_scace,
                'curr_floor': curr_floor,
                'max_floor': max_floor,
                'home_type': home_type,
                'build_year': build_year,
                'district': district,
                'serv_lift': serv_lift,
                'pass_lift': pass_lift,
                'parking': parking,
                'loggia': loggia,
                'balcony': balcony,
                'garbage_chute': garbage_chute,
                'bathroom': bathroom,
                'repair_type': repair_type,
                'wind_view': wind_view,
                'emergency_exit': emergency_exit,
                'avg_price_for_m': avg_price_for_m,
                'avg_room_price': avg_room_price,
                'price': price}
        write_csv(data)
        print('   Advertising %i complete' % i)
        i+=1
    return True



def main():
    base_url_1 = 'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&max_house_year=2019&offer_type=flat&p='
    base_url_2 = '&region=4959&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1'
    with open('apartments_cian.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('rooms',
                         'square, м²',
                         'living_space, м²',
                         'kitchen_scace, м²',
                         'curr_floor',
                         'max_floor',
                         'home_type',
                         'build_year',
                         'district',
                         'serv_lift',
                         'pass_lift',
                         'parking',
                         'loggia',
                         'balcony',
                         'garbage_chute',
                         'bathroom',
                         'repair_type',
                         'wind_view',
                         'emergency_exit',
                         'avg_price_for_m',
                         'avg_room_price',
                         'price, RUB'))
    print('start')
    start_time = time.time()
    i = 1
    while i<61:
        print('---------------- Page %i start ----------------' % i)
        url_gen = base_url_1 + str(i) + base_url_2
        #html = get_html(url_gen)
        #past_data_page(html)
        if past_data_page(url_gen):
            i+=1
            print('---------------- Page %i complete ----------------' % i)
        else:
            print('PAGE ERROR')
            crawler.rotate()
    print('finish')
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == '__main__':
    main()
