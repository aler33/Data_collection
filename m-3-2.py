# 2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
# То есть цифра вводится одна, а запрос проверяет оба поля

from pymongo import MongoClient
from pprint import pprint


def check_price(vac, num):
    for vacan in vac.find({'$or': [{'price_min': {'$gt': num}}, {'price_max': {'$gt': num}}]}):
        pprint(vacan)
    for vacan in vac.find({'$and': [{'currency': 'USD'}, {'$or': [{'price_min': {'$gt': num/60}}, {'price_max': {'$gt': num/60}}]}]}):
        pprint(vacan)
    for vacan in vac.find({'$and': [{'currency': 'EUR'}, {'$or': [{'price_min': {'$gt': num/65}}, {'price_max': {'$gt': num/65}}]}]}):
        pprint(vacan)


if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client['base220708']
    vac = db.vacancy

    numb = int(input('Введитите минимальную зарплату'))
    check_price(vac, numb)
