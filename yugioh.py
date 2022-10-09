import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup


def webscrap(count):
    url = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&sort=1&rp=100&page=1&stype=4&othercon=2&page=1'
    with open('yugioh.csv', 'w', encoding='UTF-8', newline='') as file:
        header_column = ['image_src', 'name', 'type', 'card_text',
                         'attribute', 'attribute_image', 'level', 'atk',
                         'defense',
                         'species']
        csvwriter = csv.writer(file, delimiter=',')
        csvwriter.writerow(header_column)
        while count >= 0:
            if count >= 0:
                url = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&rp=100&page='+str(count)+'&keyword=&stype=4&ctype=&othercon=2&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto='
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                body = soup.find('div', id='article_body')
                card_list = body.find('div', id='card_list')
                carddf = pd.DataFrame()
                if card_list is not None:
                    for card_index in card_list.find_all('div', {'class': 't_row c_normal'}):
                        img = card_index.find('img')
                        img_src = None
                        for index in img:
                            img_src = index['src']
                        name = card_index.find('span', {'class': 'card_name'})
                        name = name.text.strip()
                        card_type = card_index.find('span',
                                                    {'class': 'box_card_attribute'})
                        card_type = card_type.text.strip()
                        card_attribute_img = card_index.find('img', {'class': 'box_card_attribute'})
                        if card_attribute_img is not None:
                            card_attribute_img = card_attribute_img.get('src')
                        card_text = card_index.find('dd', 'box_card_text')
                        card_text = card_text.text.strip()
                        attribute = card_index.find('span', 'box_card_attribute')
                        attribute = attribute.text.strip()
                        level = card_index.find('span', 'box_card_level_rank level')
                        if level is not None:
                            level = level.text.strip()
                        atk = card_index.find('span', 'atk_power')
                        if atk is not None:
                            atk = atk.text.strip()
                        defense = card_index.find('span', 'def_power')
                        if defense is not None:
                            defense = defense.text.strip()
                        species = card_index.find('span', {
                            'class': 'card_info_species_and_other_item'})
                        if species is not None:
                            species = species.text.replace("\t", "")
                            species = species.replace("\n", "")
                            species = species.replace("\r", "")
                        row = [img_src, name, card_type, card_text, attribute,
                               card_attribute_img, level, atk, defense, species]
                        print(row)
                        csvwriter.writerow(row)
                else:
                    print("failed to find card list")
            count -= 1
        print(carddf.head())


if __name__ == '__main__':
    count = int(input("enter count: "))
    webscrap(count)
