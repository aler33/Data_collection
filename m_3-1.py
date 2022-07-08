# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo import errors


def get_data(_page):
    url = 'https://hh.ru/search/vacancy'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    params = {'search_field': ['name', 'company_name', 'description'],
              'only_with_salary': 'true',
              'text': 'Python developer',
              'page': _page}
    response = session.get(url, headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    return dom


def parce_p(dom, vacans_list, vac):
    a_link = dom.find_all('span', {'class': 'g-user-content'})
    for link in a_link:
        link_0 = list(link.children)[0].get('href')
        name_vacan = list(link.children)[0].text
        price = list(link.parent.parent.parent.children)[2].text

        if price[0] == 'о':
            num_1_2 = price.replace(u"\u202F", "")
            reg = re.findall('[\s]+[\w]+', num_1_2)
            num_1 = int(reg[0].replace(' ', ''))
            num_2 = None
            curen = reg[1].replace(' ', '')

        elif price[0] == 'д':
            num_1_2 = price.replace(u"\u202F", "")
            reg = re.findall('[\s]+[\w]+', num_1_2)
            num_2 = int(reg[0].replace(' ', ''))
            num_1 = None
            curen = reg[1].replace(' ', '')

        else:
            num_1_2 = price.replace(u"\u202F", "")
            reg = re.findall('[\d]+[\w]+', num_1_2)
            reg_1 = re.findall('[\D][\w]+', num_1_2)
            num_1 = int(reg[0].replace(' ', ''))
            num_2 = int(reg[1].replace(' ', ''))
            curen = reg_1[1].replace(' ', '')

        vacans_dic = {'name_vacansion': name_vacan,
                      'price_min': num_1,
                      'price_max': num_2,
                      'currency': curen,
                      'link': link_0,
                      'site': "HH"}
        vacans_list.append(vacans_dic)   # Теперь его можно удалить, так как не используется

        if not vac.find_one({'name_vacansion': name_vacan,
                      'price_min': num_1,
                      'price_max': num_2,
                      'currency': curen,
                      'link': link_0,
                      'site': "HH"}):
            try:                            # Скорей всего можно обойтись без try
                vac.insert_one(vacans_dic)
            except errors.DuplicateKeyError:
                pass
        else:                               # Заменяется на теже самые данные
            vac.replace_one({'name_vacansion': name_vacan,
                      'price_min': num_1,
                      'price_max': num_2,
                      'currency': curen,
                      'link': link_0,
                      'site': "HH"}, vacans_dic)
    return vacans_list


if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client['base220708']
    vac = db.vacancy

    vacansions_list = []
    session = requests.Session()
    dom = get_data(0)
    pages = dom.find_all('a', {'class': 'bloko-button', 'data-qa': 'pager-page'})
    for page in pages:
        page_max = int(list(page.children)[0].text)
    parce_p(dom, vacansions_list, vac)

    for page_num in range(1, page_max):
        print(f'Обрабатывается страница: {page_num}')
        dom = get_data(page_num)
        parce_p(dom, vacansions_list, vac)
