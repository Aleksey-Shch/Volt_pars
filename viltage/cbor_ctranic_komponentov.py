from bs4 import BeautifulSoup
import requests

# Чтение из файла и преобразовываем с soup
def read_text():
    with open('index_comp.html', 'r', encoding='utf-8') as w_file:
        src = w_file.read()
    return BeautifulSoup(src, "lxml")

#Чтение данных из сохраненного файла id="page_navigation"
soup = read_text()

# for s in soup.find('div', {'id': 'page_navigation'}).find_all('a'):
#     print(f'https://voltag.ru/{s.get("href")}')

#https://voltag.ru/components/list/?q=ALB0829
href_component_pages = []
if soup.find('div', class_='page_number_outer'):
    for s in soup.find('div', {'id': 'page_navigation'}).find_all('a'):
        print(f'https://voltag.ru{s.get("href")}')
else:
    print('нет')