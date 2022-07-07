# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json


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


def parce_p(dom, vacans_list):
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
        vacans_list.append(vacans_dic)
    return vacans_list


if __name__ == "__main__":
    vacansions_list = []
    session = requests.Session()
    dom = get_data(0)
    pages = dom.find_all('a', {'class': 'bloko-button', 'data-qa': 'pager-page'})
    for page in pages:
        page_max = int(list(page.children)[0].text)
    parce_p(dom, vacansions_list)

    for page_num in range(1, page_max):
        print(f'Обрабатывается страница: {page_num}')
        dom = get_data(page_num)
        parce_p(dom, vacansions_list)

    with open('hh.json', 'w') as f:
        json.dump(vacansions_list, f)

