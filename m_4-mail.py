# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
from pymongo import errors


def get_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    response = session.get(url, headers=headers)
    dom = html.fromstring(response.text)

    return dom


def parce_start(dom):
    a_link_3 = dom.xpath("//ul[@class='list list_type_square list_half js-module']//li[@class='list__item']/a/@href")
    a_link_2 = dom.xpath("//a[@class='photo photo_small photo_scale photo_full js-topnews__item']/@href")
    a_link = dom.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")
    a_link.extend(a_link_2)
    a_link.extend(a_link_3)

    return a_link


def parce_news(dom, url, news):
    news_source = dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span[@class='link__text']/text()")
    news_article = dom.xpath("//h1[@class='hdr__inner']/text()")
    news_date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    news_hash = hash(url)

    news_dic = {'_id': news_hash,
                'news_source': news_source[0],
                'news_article': news_article[0],
                'URL': url,
                'news_date': news_date[0]}
    pprint(news_dic)

    if not news.find_one({'URL': url}):
        try:
            news.insert_one(news_dic)
        except errors.DuplicateKeyError:
            pass
    else:
        print(f'Новость "{news_article[0]}" уже есть в базе данных')


if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client['base220712']
    news = db.news

    url = 'https://news.mail.ru/?_ga=2.112044676.1646148374.1657535084-2055804998.1656687070y'
    session = requests.Session()
    dom = get_data(url)
    news_url = parce_start(dom)

    for url in news_url:
        dom = get_data(url)
        parce_news(dom, url, news)
