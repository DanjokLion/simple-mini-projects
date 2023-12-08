from bs4 import BeautifulSoup
import random, json, requests, datetime
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'accepts': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}
article_dict = {}
url = f'https://habr.com/ru/top/daily/'

req = requests.get(url, headers=headers).text
soup = BeautifulSoup(req, 'lxml')
hrefArticles = soup.find_all('a', class_='tm-title__link')

for art in hrefArticles:
    article_name = art.find('span').text
    article_link = f'https://habr.com{art.get("href")}'

    article_dict[article_name] = article_link

with open(f'articles_{datetime.datetime.now().strftime("%d_%m_%Y")}.json', 'w', encoding='utf-8') as file:
    try:
        json.dump(article_dict, file, indent=4, ensure_ascii=False)
        print('Статьи получены')
        for key, value in article_dict.items():
            print(f'{key} - {value}')
    except:
        print('Статьи получить не удалось')

