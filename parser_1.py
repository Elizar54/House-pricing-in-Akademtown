from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2
import re


def set_chrome_options():
    """
    Sets chrome chrome_options for Selenium.
    Chrome chrome_options for headless browser is enabled.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36')
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-gpu")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

print('старт')
conn = psycopg2.connect(host='ep-black-pond-a2ydwdvs.eu-central-1.aws.neon.tech', database='Akademdb', user='Elizar54', password='XUpC1QOnGvA4')
cur = conn.cursor()

URL = 'https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4897&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1'
link_list = []
p = 516
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=set_chrome_options())
wait = WebDriverWait(driver, 10)

while len(link_list) < 5000:
    if p % 10 == 0:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=set_chrome_options())
    driver.get(URL)
    html = driver.page_source
    all_links = re.findall('https://novosibirsk.cian.ru/sale/flat/[0-9]{9}/', html)
    link_list += list(set(all_links))
    p += 1
    URL = f'https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={p+1}&region=4897&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1'


print('ссылки выгружены', p)
id = 14449

columns = set(('id', 'Общая площадь', 'Этаж', 'Год сдачи', 'Дом', 'Отделка', 'price', 'metro', \
                'address', 'Жилая площадь', 'Площадь кухни', 'Высота потолков', 'Балкон/лоджия', \
                    'Вид из окон', 'Санузел', 'Тип дома', 'Мусоропровод', 'Отопление', 'Подъезды', \
                          'Аварийность', 'Тип перекрытий', 'Количество лифтов', 'Строительная серия'))

for link in link_list:
    if id % 100 == 0:
        conn = psycopg2.connect(host='ep-black-pond-a2ydwdvs.eu-central-1.aws.neon.tech', database='Akademdb', user='Elizar54', password='XUpC1QOnGvA4')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=set_chrome_options())

    try:    
        driver.get(link)
        flat = {}
        address_str = ''

        flat['id'] = id

        address = driver.find_elements(By.CLASS_NAME, 'a10a3f92e9--address--SMU25')
        for elem in address:
            address_str += elem.text + ' '

        if not('Кировский' in address_str or 'Ленинский' in address_str):
            elements = driver.find_elements(By.CLASS_NAME, 'a10a3f92e9--item--Jp5Qv')
            
            if elements == []:
                descript = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--group--K5ZqN')
                elements = descript.find_elements(By.CLASS_NAME, 'a10a3f92e9--item--qJhdR')
            
            price = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--amount--ON6i1')

            home_elems = driver.find_elements(By.CLASS_NAME, 'a10a3f92e9--item--qJhdR')
            
            if home_elems != []:
                for elem in home_elems:
                    elem_lst = elem.text.split('\n')
                    flat[elem_lst[0]] = elem_lst[1]

            try:
                metro = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--undergrounds--sGE99')
            except:
                pass

            for elem in elements:
                elem_lst = elem.text.split('\n')
                flat[elem_lst[0]] = elem_lst[1]
            
            flat['price'] = price.text
            flat['metro'] = metro.text
            flat['address'] = address_str

            
            
            if 'Тип жилья' in set(flat.keys()): 
                flat['Дом'] = flat['Тип жилья'] 
                del flat['Тип жилья']

            for key in columns - set(flat.keys()):
                flat[key] = 'None' 

            if flat['metro'] == '':
                flat['metro'] = 'None'

            if 'Год постройки' in set(flat.keys()): del flat['Год постройки']

            id += 1
            
            with conn.cursor() as curs:
                tuple_insert = (flat['id'], flat['Общая площадь'], flat['Этаж'], flat['Год сдачи'], flat['Дом'], flat['Отделка'],\
                                            flat['price'], flat['metro'], flat['address'], flat['Жилая площадь'], flat['Площадь кухни'], \
                                            flat['Высота потолков'], flat['Санузел'], flat['Балкон/лоджия'], flat['Вид из окон'], flat['Тип перекрытий'], \
                                            flat['Мусоропровод'], flat['Тип дома'], flat['Отопление'], flat['Подъезды'], flat['Аварийность'], flat['Количество лифтов'])
                curs.execute("INSERT INTO flats_new (id, total_square, floor, year, rented, decor, price, metro, address, living_sq, kitchen_sq, ceil_height, \
                                        toilets, balcony, window_view, barriers, trash, home_type, warm, entrance, warning, elevators) VALUES (%s, %s, %s, \
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tuple_insert)
                conn.commit()
    except:
        pass