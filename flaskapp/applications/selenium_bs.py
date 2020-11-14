from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import lxml
import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from selenium.webdriver.chrome.options import Options

# import time

# def make_list(soup):
#     cars = soup.select("div[class='textBox']")

#     car_list = []
#     for car in cars:
#         car_dict = {}
#         name = car.select("span[class='CarName']")[0].text
#         desc = car.select("span[class='CarDesc']")[0].text
#         car_dict['car_name'] = name + desc
#         car_dict['base_price'] = car.select("div[class='base_price'] > dl:first-child >dd")[0].text
#         car_dict['total_price'] = car.select("dd[class='f_color_red']")[0].text
#         car_dict['store_name'] = car.select("p[class='store_name']")[0].text
#         car_dict['store_tel'] = car.select("p[class='store_tel']")[0].text[2:]
#         car_list.append(car_dict)
#     details = soup.select("div[class='detailsArea']")
#     details_list = []
#     for i in range(len(details)):
#         details_list.append(details[i].text)
#     a_list = []
#     for i in range(len(details_list)):
#         detail_list = [v.strip() for v in re.split('[ \n]', details_list[i]) if v]
#         a_list.append(detail_list)
#     d_list = []
#     for i in a_list:
#         if len(i) == 12:
#             details_dict = {}
#             details_dict['year'] = f'{i[0]}:{i[1]}'
#             details_dict['runs'] = f'{i[2]}:{i[3]}'
#             details_dict['displacement'] = f'{i[4]}:{i[5]}'
#             details_dict['repair'] = f'{i[6]}:{i[7]}'
#             details_dict['warranty'] = f'{i[8]}:{i[9]}'
#             details_dict['mission'] = f'{i[10]}:{i[11]}'
#             d_list.append(details_dict)
#         else:
#             d_list.append({})
#     for i, j in zip(car_list, d_list):
#         i.update(j)

#     return car_list

# def seleniumbs(keywords):
#     driver = webdriver.Chrome("chromedriver_win32/chromedriver.exe")
#     driver.implicitly_wait(3)
#     url = 'https://www.goo-net.com/'
#     driver.get(url)
#     search_field = driver.find_element_by_xpath("//input[@id='phrase_input']")
#     search_field.send_keys(keywords)
#     search_field.send_keys(Keys.ENTER)
#     responses = []
#     response = driver.page_source
#     soup = bs(response, 'lxml')
    
#     car_list = make_list(soup)
    
#     next_button = driver.find_element_by_xpath("//div[@class='pager']/ul/li[@class='next']")
#     time.sleep(5)
#     while next_button:
#         next_button.click()
#         time.sleep(3)
#         driver.get(driver.current_url)
#         response = driver.page_source
#         soup = bs(response, 'lxml')
#         another_car_list = make_list(soup)
#         car_list.extend(another_car_list)
#     driver.close()

#     return car_list



def seleniumbs(keywords):
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    url = 'https://www.goo-net.com/'
    driver.get(url)
    search_field = driver.find_element_by_xpath("//input[@id='phrase_input']")
    search_field.send_keys(keywords)
    search_field.send_keys(Keys.ENTER)
    response = driver.page_source
    driver.close()
    soup = bs(response, 'lxml')

    cars = soup.select("div[class='textBox']")

    car_list = []
    car_data = []
    for car in cars:
        car_dict = {}
        name = car.select("span[class='CarName']")[0].text
        desc = car.select("span[class='CarDesc']")[0].text
        car_dict['car_name'] = name + desc
        car_dict['base_price'] = car.select("div[class='base_price'] > dl:first-child >dd")[0].text[:-2]
        car_dict['total_price'] = car.select("dd[class='f_color_red']")[0].text[:-2]
        car_dict['store_name'] = car.select("p[class='store_name']")[0].text
        car_dict['store_tel'] = car.select("p[class='store_tel']")[0].text[2:]
        car_dict['url'] = 'https://www.goo-net.com/usedcar/spread/goo/18/' + car.select(" input[name='id']")[0].attrs['value'] + '.html'
        car_list.append(car_dict)
    details = soup.select("div[class='detailsArea']")
    details_list = []
    for i in range(len(details)):
        details_list.append(details[i].text)
    a_list = []
    for i in range(len(details_list)):
        detail_list = [v.strip() for v in re.split('[ \n]', details_list[i]) if v]
        a_list.append(detail_list)
    d_list = []
    for i in a_list:
        if len(i) == 12:
            details_dict = {}
            details_dict['details'] = True
            details_dict['year'] = f'{i[1]}'
            details_dict['runs'] = f'{i[3][:-2]}'
            details_dict['displacement'] = f'{i[5][:-2]}'
            details_dict['repair'] = f'{i[6]}{i[7]}'
            details_dict['warranty'] = f'{i[8]}:{i[9]}'
            details_dict['mission'] = f'{i[10]}{i[11]}'
            d_list.append(details_dict)
        else:
            details_dict = {}
            details_dict['details'] = False
            d_list.append(details_dict)
    for i, j in zip(car_list, d_list):
        i.update(j)

    return car_list

def seleniumbs_plt(car_list):
    car_data = []
    for i in car_list:
        data_dict = {}
        if i['details']:
            data_dict['base_price'] = i['base_price']
            data_dict['year'] = i['year'][:4]
            if '万' in i['runs'] :
                data_dict['runs'] = (i['runs'][:-1])
            else:
                data_dict['runs'] = str(float(i['runs'])/10000)
        else:
            data_dict['base_price'] = 0.1
            data_dict['runs'] = '0.1'
            data_dict['year'] = '2000'
        car_data.append(data_dict)
    
    plt.figure(figsize=(6, 4))
    plt.title('base_price, year, runs', fontdict={'fontname':'Sans serif', 'fontsize':15})
    plt.xlabel('index', fontdict={'fontname':'Sans serif', 'fontsize':8})
    plt.ylabel('base_price', fontdict={'fontname':'Sans serif', 'fontsize':12})
    plt.xticks(np.arange(1, len(car_data)+1, 1), rotation=90)

    x = [ car_data.index(i)+1 for i in car_data ]
    y = [ float(i['base_price']) for i in car_data]
    colors = [ round(float(i['runs'])) for i in car_data]
    sizes = [ (int(i['year'])-1980)**3/300 for i in car_data ]
    plt.scatter(x, y, s=sizes, c=colors, cmap='Greens', edgecolor='black', linewidths=1, alpha=0.8, marker='o', vmin=0, vmax=10)
    plt.colorbar()
    plt.grid(alpha=0.6, linewidth=0.5, color='red')
    d = datetime.now()
    time = f'{d:%Y%m%d%H%M%S}'
    plt.savefig(f'flaskapp/static/images/selenium_bs/{time}.jpeg', dpi=480)

    return time

