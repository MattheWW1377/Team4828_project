import pandas as pd
import requests
from bs4 import BeautifulSoup

# Ссылка на сайт
url = "https://scholar.google.com/scholar?hl=ru&as_sdt=0%2C5&q=проектная+деятельность+в+образовании&oq=Проектная+деятельность"


# Функция, которая выводит заголовки найденных запросов
def parsing_headers(url):
    # Отправляем запрос на сайт и получаем ответ
    r = requests.get(url)
    # Создаем объект BeautifulSoup для парсинга HTML-кода сайта
    soup = BeautifulSoup(r.content, 'html.parser')

    headers_text = []
    headers = soup.find_all('h3')
    for header in headers:
        headers_text.append(header.text)
    return headers_text


# Функция, которая выводит ссылки найденных запросов
def parsing_links(url):
    # Отправляем запрос на сайт и получаем ответ
    r = requests.get(url)
    # Создаем объект BeautifulSoup для парсинга HTML-кода сайта
    soup = BeautifulSoup(r.content, 'html.parser')

    links = soup.find_all('a', id=True, href=True, attrs={"data-clk": True})
    links_text = []
    for link in links:
        links_text.append(link.get('href'))
    return links_text


# Функция, которая проходит по всем страницам найденного запроса
def parsing_page(url):
    # Отправляем запрос на сайт и получаем ответ
    r = requests.get(url)
    # Создаем объект BeautifulSoup для парсинга HTML-кода сайта
    soup = BeautifulSoup(r.content, 'html.parser')

    pages = soup.find_all('a', class_='gs_nma')
    page_text = []
    for page in pages:
        page_text.append(page.get('href'))

    i = 0
    for page in page_text:
        page = 'https://scholar.google.com/' + page
        page_text[i] = page
        i += 1

    return page_text


# Функция, которая находит ссылку на цитируемые статьи
def quote(url):
    # Отправляем запрос на сайт и получаем ответ
    r = requests.get(url)
    # Создаем объект BeautifulSoup для парсинга HTML-кода сайта
    soup = BeautifulSoup(r.content, 'html.parser')

    links = soup.find_all('a', href=True)
    links_text = []
    for link in links:
        links_text.append(link.get('href'))
    citata = []
    for i in links_text:
        if "/scholar?cites=" in i:
            i = "https://scholar.google.com" + i
            citata.append(i)
    quot = []
    for q in citata:
         quot.append([parsing_links(q)])
    return quot
    # return citata

# Создание словаря и csv файла
dict = {'Headings': parsing_headers(url), 'Links': parsing_links(url), 'Quote': quote(url)}

for ind in parsing_page(url):
    headers = []
    links = []
    quotes = []
    headers.append(parsing_headers(ind))
    for pages in headers:
        for header in pages:
            dict['Headings'].append(header)
    links.append(parsing_links(ind))
    for pages2 in links:
        for link in pages2:
            dict['Links'].append(link)
    quotes.append(quote(ind))
    for pages3 in quotes:
        for quot in pages3:
            dict['Quote'].append(quot)

df = pd.DataFrame(dict)
df.to_csv('file1.csv')

print(df)
# print(dictionary(parsing_headers(url), parsing_links(url), quote(url)))
# print(page_enumeration(parsing_page(url)))
