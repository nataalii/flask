import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint


def get_paintings():
    result = []

    for ind in range(1, 3):
        url = "https://daraba.art/ge/artworks?categories=4&priceFrom=0&minPeriod=1910&maxPeriod=2020&minWidth=1&maxWidth=" \
              "200&minHeight=1&maxHeight=200&priceTo=8480&material=&medium=&color=&subject=&sort=&discover=&page=" +\
              str(ind)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        all_painting = soup.find('div', id='product-list')
        paintings = all_painting.find_all('div', class_='article-item')

        for painting in paintings:
            p_features = painting.find('div', class_='title-container')
            p_price = painting.find('span', class_='new-price').text.strip()
            p_title = p_features.h4.a.text.strip()
            p_author = p_features.h6.a.text.strip()
            result.append({'title': p_title, 'author': p_author, 'price': p_price})

    return result



