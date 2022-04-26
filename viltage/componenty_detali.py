# https://voltag.ru/catalog/group/voltag_alb0829_generator/ - основной сайт
# https://voltag.ru/components/list/?q=ALB0829 - компоненты
from bs4 import BeautifulSoup
import requests
import re


model = 'ALA0785' # Два листа компонентов
#model = 'ala3231' 'ala2610'# нет компонентов совсем
# чтение данных с сайта и сохранение в файле html
def reader_url_saved_text(url, kol):
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
    try:
        with open(f"{kol}_index_comp_{model}.html", "w", encoding="utf-8") as file:
            file.write(text_html)
            return BeautifulSoup(text_html, "lxml")
    except Exception:
        print(f"Ошибка при сохранении файла")

# Чтение из файла html и преобразовываем с soup
#def read_text(kol):
#    try:
#        with open(f"{kol}_index_comp_{model}.html", 'r', encoding='utf-8') as w_file:
#            src = w_file.read()
#        return BeautifulSoup(src, "lxml")
#    except Exception as err:
#        print(f'Нет такого файла - index_comp_{kol}.html. Ошибка {err}')

# поиск всех компонентов на странице с их ссылками
def saved_component_ctranica(soup, n):
    href_componenta = soup.find('div', class_='catalog_list').find_all('div', {'class': re.compile("catalog_item ")})
    n = 1
    for s in href_componenta:  # [0]:
        #print(f'{n}' - {s}')
        #    href_comp = s.find('div', class_='catalog_item_title').get('href')
        href_comp = 'https://voltag.ru' + s.find('a').get('href')
        nomer_comp = (s.find('div', class_='catalog_item_title_wrap').text).replace("\n","")
        nazvanie_comp = s.find('div', class_='catalog_item_subtitle').text
        print(f'{n} - {nomer_comp} - {nazvanie_comp} - {href_comp}') #, sep="\n")
        n += 1
    return n

#Сохраняем первую страницу
stranica = 1
soup = reader_url_saved_text(f"https://voltag.ru/components/list/?q={model}", stranica)


#Чтение данных из сохраненного файла
#soup = read_text(stranica)


# Проверияем сколько страниц, если не одна сохраняем все
n = 1
if soup.find('div', class_='page_number_outer'):
    n = saved_component_ctranica(soup,n)
    stranica += 1
    print(f"Много листов - {stranica}")
    for s in soup.find('div', {'id': 'page_navigation'}).find_all('a'):
        sopu = reader_url_saved_text(f'https://voltag.ru{s.get("href")}', stranica)
        # тут надо сделать чтение всей станицы в файл
        n = saved_component_ctranica(soup, n)
        stranica+=1
else:
    # тут надо сделать чтение всей станицы в файл
    print(f"Один листов - {stranica}")
    n = saved_component_ctranica(soup, n)