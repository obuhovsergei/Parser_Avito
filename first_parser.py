import requests
from bs4 import BeautifulSoup as bs
import csv
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }

base_url = 'https://www.avito.ru/kazan/tovary_dlya_kompyutera/komplektuyuschie/videokarty?cd=1&pmax=7000&pmin=2000'
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
            if title != 'Видеокарта':
                dlist = {}
                dlist['title'] = title
                dlist['price'] = price
                dlist['href'] = href
                data.append(dlist)
        with open('VideoCards.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0])
            writer.writeheader()
            writer.writerows(data)
        print('Файл сохранён')
    else: print('Ошибка')
parse(base_url, headers)