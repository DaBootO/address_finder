from bs4 import BeautifulSoup
import requests

BASE_PRESSEPORTAL_URL = "https://www.presseportal.de"
STARTER = "/suche/Geldautomat/blaulicht"

URL_PLACE_ARTICLE_LIST = []

raw_text = requests.get(BASE_PRESSEPORTAL_URL + STARTER).text

soup = BeautifulSoup(raw_text, 'html.parser')
found_articles = 0

while soup.find('link', rel='next'):
    article_list = soup.findAll('article', class_='news')
    for article in article_list:    
        if 'data-url-ugly' in article.attrs.keys():
            url = article.attrs['data-url-ugly'].replace('@', '/')
        else:
            continue
        if article.find(attrs={"data-label":'cityClick'}):
            place = article.find(attrs={"data-label":'cityClick'}).text
        else:
            place = 'NaN'
        print(f'{url:10} ### {place: ^20}')
        URL_PLACE_ARTICLE_LIST.append([url, place])
        found_articles += 1
    FOLLOW_NEXT = soup.find('link', rel='next').attrs['href']
    raw_text = requests.get(BASE_PRESSEPORTAL_URL + FOLLOW_NEXT).text
    soup = BeautifulSoup(raw_text, 'html.parser')

print(f'We found {found_articles: ^6} articles!')

with open('url_data.dat','w') as f:
    for line in URL_PLACE_ARTICLE_LIST:
        f.write(line[0] + ',' + line[1] + '\n')