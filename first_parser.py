import requests
from bs4 import BeautifulSoup as bs
import csv
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
def choise ():
    print("---Категория поиска---\n1) Видеокарты\n2) Материнские платы\n3) Оперативная память\n4) Процессоры\n5) Накопители")
    category = int(input('Введите категорию поиска: '))
    min = int(input('Введите минимальную цену (Р): '))
    max = int(input('Введите максимальную цену (Р): '))
    if max <= min: raise ValueError('Макисмальная цена не может быть меньше или равняться минимальной!')
    if   category == 1: cat_use = "videokarty"
    elif category == 2: cat_use = "materinskie_platy"
    elif category == 3: cat_use = "operativnaya_pamyat"
    elif category == 4: cat_use = "protsessory"
    elif category == 5: cat_use = "zhestkie_diski"
    else: raise ValueError('Ошибка ввода категории, требуется ввести числа от 1 до 5')
    return 'https://www.avito.ru/kazan/tovary_dlya_kompyutera/komplektuyuschie/' + cat_use + '?cd=1&pmax=' + str(max) + '&pmin=' + str(min)
def parse (base_url, headers):
    data = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        parser = bs(request.content, 'html.parser')
        divs = parser.find_all('div', attrs={
            'data-marker': 'item',
            'class': 'item-with-contact'
        })
        for div in divs:
            title = div.find('span', attrs={'itemprop': 'name'}).text
            price = div.find('span', attrs={'itemprop': 'price'}).text.strip()[:-3]
            href = 'https://www.avito.ru/' + div.find('a', attrs={'itemprop': 'url'})['href']
            dlist = {}
            dlist['title'] = title
            dlist['price'] = price
            dlist['href'] = href
            data.append(dlist)
        with open('VideoCards.csv', 'w', newline='') as file: #Saving in file
            writer = csv.DictWriter(file, fieldnames=data[0])
            writer.writeheader()
            writer.writerows(data)
        print('Файл сохранён')
    else: print('Ошибка соединения')
parse(choise(), headers) #Parse avito and save in file CSV