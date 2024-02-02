import requests
from bs4 import BeautifulSoup
import asyncio

DOMEN = 'https://hdrezkayh3h2p.org'
async def name_find_film(name:str) -> list:
    films_info_list = []
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    data = {'do': 'search', 'subaction': 'search', 'q': name}
    response = requests.post(f'{DOMEN}/search/', data=data, headers=headers)
    print(response)
    html_string = response.text
    soup = BeautifulSoup(html_string, 'html.parser')

    film_object_list = soup.find_all('div', class_='b-content__inline_item')
    id = 0
    for film_object in film_object_list:
        print(film_object)
        url = film_object.find('a')['href']
        type = film_object.find('i', class_='entity').text
        image_src = film_object.find('img')['src']
        title = film_object.find('div', class_='b-content__inline_item-link').a.text
        year_country_genre = film_object.find('div', class_='b-content__inline_item-link').div.text
        try:
            last_series = film_object.find('span', class_='info').text
        except AttributeError:
            is_serial = False
        else:
            is_serial = True
        films_info_list.append([image_src, title, year_country_genre, type, url, id,is_serial])
        id = id + 1
        print(f"Image Source: {image_src}")
        print(f"Title: {title}")
        print(f"Year, Country, Genre: {year_country_genre}")
        print(f"Type: {type}")
        print(f"URL: {url}")
        print(f"ID: {id}")
        print(f'is_serial {is_serial}')
        print('-' * 100)
    #print(films_info_list)
    return films_info_list



# asyncio.run(name_find_film('Звездие войни'))






