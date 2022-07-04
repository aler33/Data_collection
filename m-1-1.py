# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json


url = 'https://api.github.com/users/aler33/repos'
response = requests.get(url)
j_data = response.json()

with open('github.json', 'w') as f:
    json.dump(j_data, f)

print('Список репозитариев:')
for rep in j_data:
    print(rep['name'])

