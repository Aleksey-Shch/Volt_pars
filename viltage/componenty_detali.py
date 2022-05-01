# https://voltag.ru/catalog/group/voltag_alb0829_generator/ - основной сайт
# https://voltag.ru/components/list/?q=ALB0829 - компоненты
from bs4 import BeautifulSoup
import requests
import re


# чтение данных с сайта и сохранение в файле html
def reader_url_component(url):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
# другой комп           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75 (Edition Yx)"
        }
        reg = requests.get(url, headers=headers)
        text_html = reg.text
    except Exception:
        print(f"Ошибка при чтении страницы {url}")
    return BeautifulSoup(text_html, "lxml")

# поиск всех компонентов на странице с их ссылками
def saved_component_ctranica(soup):
    # проверка на наличие компонентов
    if soup.find('div', class_ = 'catalog_item_title_wrap'):
        href_componenta = soup.find('div', class_='catalog_list').find_all('div', {'class': re.compile("catalog_item ")})
        #n = 1 catalog_item_title_wrap
        for s in href_componenta:  # [0]:
            #print(f'{n}' - {s}')
            #    href_comp = s.find('div', class_='catalog_item_title').get('href')
            href_comp = 'https://voltag.ru' + s.find('a').get('href')
            nomer_comp = (s.find('div', class_='catalog_item_title_wrap').text).replace("\n","")
            nazvanie_comp = s.find('div', class_='catalog_item_subtitle').text
            #print(f'{nomer_comp} - {nazvanie_comp} - {href_comp}') #, sep="\n")
            spisok_componentov[nomer_comp] = [nazvanie_comp, href_comp]
            # #Запись данных в файл формата json
            # with open(f'cross_{quotes_model}.json', 'w') as j_file:
            #     json.dump(cross, j_file, indent=4, ensure_ascii=False)
        return
    print('ничего нет')

#Перебираем все страницы и сохраняем список компонентов
# Проверияем сколько страниц, если не одна сохраняем все
def perebor_pages_component(soup):
    if soup.find('div', class_='page_number_outer'):
        print(f"Много листов ")
        saved_component_ctranica(soup)
        for s in soup.find('div', {'id': 'page_navigation'}).find_all('a'):
            # print(f"Много листов - {stranica}")
            soup_list = reader_url_component(f'https://voltag.ru{s.get("href")}')
            # тут надо сделать чтение всей станицы в файл
            saved_component_ctranica(soup_list)
    else:
        # тут надо сделать чтение всей станицы в файл
        # print(f"Один листов - {stranica}")
        saved_component_ctranica(soup)
        print('Все!')

def update_dictionary(d, key, value):
    # put your python code here
    if d.get(key) == None:
        d[key]=(value)


spisok_componentov={}
model = 'ALA0879' # три листа компонентов
#model = 'ala3231' 'ala2610' 'ALA0785' 'ALA0879' # нет компонентов совсем
#Сохраняем первую страницу
soup = reader_url_component(f"https://voltag.ru/components/list/p-1/?q={model}")
perebor_pages_component(soup)

for keys, values in spisok_componentov.items():
    print(f'{keys} - {values}')
