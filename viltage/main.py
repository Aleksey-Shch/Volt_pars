import json
import os.path
import requests
from bs4 import BeautifulSoup
import openpyxl

# чтение данных с сайта и сохранение в файле
def reader_url_saved_text(url):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
        }
        reg = requests.get(url, headers=headers)
        text_html = reg.text
    except Exception:
        print(f"Ошибка при чтении страницы {url}")
    try:
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(text_html)
    except Exception:
        print(f"Ошибка при сохранении файла")

# reader_url_saved_text("https://voltag.ru/catalog/group/voltag_ala0236_generator/?q=ALA0236")
#reader_url_saved_text("https://voltag.ru/catalog/list/voltag_ala2610_generator/?q=ala2610")
# Вводим адрес и созраняем в фалйе через функцию
url_detali = input("Введите адрес страница с сата voltag.ru")
if len(url_detali) > 20 and url_detali.find("https://voltag.ru") == 0:
    reader_url_saved_text(url_detali)
else:
    print("Проверьте адрес. ")

# Чтение из файла и преобразовываем с soup
def read_text():
    try:
        with open('index.html', 'r', encoding='utf-8') as w_file:
            src = w_file.read()
        return BeautifulSoup(src, "lxml")
    except Exception as err:
        print(f"Ошибка чтения из файла. Ошибка {err}")

#Чтение данных из сохраненного файла
soup = read_text()

# фильтрация данных характеристики
quotes_harakteristika = soup.find('div', class_='catalog_group_params').find_all('tr')
# фильтрация данных кроссов
quotes_kross = soup.find('div', class_='catalog_group_crosslist_info')
# фильтраци данных применимости
quotes_primenimost = soup.find('div', class_='catalog_group_application_info')
# фильтрация названия модели
model = ''.join(soup.find('div', class_='catalog_group_title').text.split())
#quotes_model1 = ''.join(quotes_model.split())
#print(quotes_primenimost)

#форматирование данных характеристики haratkeristika
haratkeristika = []
for znac in quotes_harakteristika:
    data = [x.get_text().replace('\xa0', ' ') for x in znac.find_all('td')]
    if len(data) != 0:
        haratkeristika.append(data)
#print(haratkeristika, '-')

#форматирование данных кроссов cross
cross = {}
katal = 'Zero'
for td in quotes_kross.find_all('td'):
    znac = td.text.strip()
    if str(td).find('mnfr') == -1:
        #print(len(znac.split(', ')))
        if len(znac.split(', '))==1:
            cross[katal]=znac
        else:
            for td1 in (znac.split(', ')):
                cross.setdefault(katal, []).append(td1)
    else:
        if znac =='':
            katal = 'Zero'
        else:
            katal=znac
#print(cross)

# #Запись данных в файл формата json
# with open(f'cross_{quotes_model}.json', 'w') as j_file:
#     json.dump(cross, j_file, indent=4, ensure_ascii=False)

#форматирование данных применимости primenimost
primenimost = [[x.replace('\t', ' ')] for x in quotes_primenimost.text.split('\n')]
#print(primenimost)

# запись данных в файл
try:
    if os.path.isfile('team.xlsx'): # Если файл сужествует открываем для записи
        excel_file = openpyxl.load_workbook('team.xlsx')
        shet_names = excel_file.sheetnames
        if model in shet_names: # проверияем существует ли лист с такой деталью
            print('Yes')
            excel_sheet = excel_file[model]
        else:
            print('No')
            excel_sheet = excel_file.create_sheet(title=model)
    else: # Иначе открываем пустой и формуем лист
        excel_file = openpyxl.Workbook()
        excel_sheet = excel_file.create_sheet(title=model)


    #Установки ширины столбцов
    excel_sheet.column_dimensions["A"].width = 18
    excel_sheet.column_dimensions["B"].width = 18
    excel_sheet.column_dimensions["C"].width = 5
    excel_sheet.column_dimensions["D"].width = 5
    excel_sheet.column_dimensions["E"].width = 30
    excel_sheet.column_dimensions["F"].width = 8
    excel_sheet.column_dimensions["G"].width = 5
    excel_sheet.column_dimensions["H"].width = 5
    excel_sheet.column_dimensions["I"].width = 50

    # Запись сроссов в файл
    excel_sheet.cell(row=1, column=1).value = 'Аналоги -' # Шиниа 20 -добавить пожзже форматирование
    excel_sheet.cell(row=1, column=2).value = model
    i=3
    for katalo, nomra in cross.items():
        if isinstance(nomra,str):
            excel_sheet.cell(row=i, column=1).value = katalo
            excel_sheet.cell(row=i, column=2).value = nomra
            i+=1
        else:
            for nomer in nomra:
                excel_sheet.cell(row=i, column=1).value = katalo
                excel_sheet.cell(row=i, column=2).value = nomer
                i += 1

    # """
    # Запись даннаых характеристики в файл
    excel_sheet.cell(row=1, column=4).value = 'Характеристика детали'

    i=3
    for harakter in haratkeristika:
        r=4
        for znacgenie in harakter:
            excel_sheet.cell(row=i, column=r).value = znacgenie
            r+=1
        i+=1

    # Запись примениомсти
    excel_sheet.cell(row=1, column=9).value = 'Список применимости:'

    i=3
    for avto in primenimost:
        excel_sheet.cell(row=i, column=9).value = ''.join(avto).strip()
        i+=1

    excel_file.save('team.xlsx')
except Exception as error:
        print('Ошибка в формировании и сохранении файла: ' + repr(error))