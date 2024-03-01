from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import psycopg2
from natasha import AddrExtractor
import pymorphy2


def price_corr(price):
    price_str = ''
    elements = price.split()
    for x in elements[:len(elements)-1]:
        price_str += x 
    return int(price_str)

def square_corr(total_sq):
    if total_sq != 'None':
        total_sq = total_sq.replace(',', '.')
        total = total_sq.split()
        return float(total[0])
    else:
        return total_sq

def addres_corr(address):
    extractor = AddrExtractor()

    matches = extractor(address)

    for match in matches:
        addres_lst = match.fact.parts[0].name.split()
        if 'Красный' in set(addres_lst):
            return 'Красный проспект'
        elif 'н' in set(addres_lst) or 'Берег' in set(addres_lst):
            return addres_lst[-1]
        elif 'жилой' in addres_lst:
            return 'жилой'
        
        return match.fact.parts[0].name


URL = 'https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4897&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1'
link_list = []
p = 0

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(0.05)

while len(link_list) < 10000:
    time.sleep(0.05)
    html = driver.find_element(By.TAG_NAME, "html")
    time.sleep(0.05)

    for k in range(400):
        html.send_keys(Keys.DOWN)

    offers = driver.find_elements(By.CLASS_NAME, '_93444fe79c--link--VtWj6')

    for elem in offers:
        link_list.append(elem.get_attribute('href'))

    p += 1
    next_page = f'https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={p+1}&region=4897&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1'
    driver.get(next_page)


flat_list = []
driver = webdriver.Chrome(options=options)
id = 0

for link in link_list:
    driver.get(link)
    time.sleep(0.5)
    flat = {}
    address_str = ''

    flat['id'] = id

    descript = driver.find_element(By.XPATH, '//*[@id="frontend-offer-card"]/div/div[2]/div[2]/div[3]')
    elements = descript.find_elements(By.CLASS_NAME, 'a10a3f92e9--item--Jp5Qv')
    
    price = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--amount--ON6i1')

    while price.text == '':
        price = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--amount--ON6i1')

    address = driver.find_elements(By.CLASS_NAME, 'a10a3f92e9--address--SMU25')

    try:
        metro = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--undergrounds--sGE99')
    except:
        pass

    for elem in address:
        address_str += elem.text + ' '

    for item in elements:
        item = item.text.split('\n')
        flat[item[0]] = item[1]
    
    flat['price'] = price.text
    flat['metro'] = metro.text
    flat['address'] = address_str
    flat_list.append(flat)
    id += 1

# data preparation

columns = set(('id', 'Общая площадь', 'Этаж', 'Год сдачи', 'Дом', 'Отделка', 'price', 'metro', 'address', 'Жилая площадь', 'Площадь кухни'))

for flat in flat_list:
    for key in columns - set(flat.keys()):
        flat[key] = 'None' 

    if flat['metro'] == '':
        flat['metro'] = 'None'
    if 'Год постройки' in set(flat.keys()): del flat['Год постройки']



for flat in flat_list:
    flat['address'] = addres_corr(flat['address'])

    if flat['Жилая площадь'] != 'None':
        flat['Жилая площадь'] = square_corr(flat['Жилая площадь'])
    
    if flat['Площадь кухни'] != 'None':
        flat['Площадь кухни'] = square_corr(flat['Площадь кухни'])
    
    if flat['Общая площадь'] != 'None':
        flat['Общая площадь'] = square_corr(flat['Общая площадь'])

    flat['price'] = price_corr(flat['price'])



conn = psycopg2.connect(host='localhost', database='flats', user='postgres', password='2109')
cur = conn.cursor()


with conn.cursor() as curs:
    for item in flat_list:
        tuple_insert = tuple((item['id'], item['Общая площадь'], item['Этаж'], item['Год сдачи'], item['Дом'], item['Отделка'],\
                              item['price'], item['metro'], item['address'], item['Площадь кухни'], item['Жилая площадь']))
        curs.execute("INSERT INTO flats (id, total_square, floor, year, rented, decor, price, metro, address, living_sq, kitchen_sq) VALUES (%s, %s, %s, \
                    %s, %s, %s, %s, %s, %s, %s, %s)", tuple_insert)
        conn.commit()
