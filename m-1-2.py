# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
#  Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
#  Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

import requests
from pprint import pprint
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url = 'https://api.vk.com/method/groups.get'
params = {'user_id': '738065396',
          'access_token': 'Здесь я убрал свой токен',
          'v': '5.131'}
response = requests.get(url, headers=headers, params=params)
j_data = response.json()

with open('vk.json', 'w') as f:
    json.dump(j_data, f)

pprint(j_data)
# {'response': {'count': 3, 'items': [41922026, 211154316, 10905291]}}

