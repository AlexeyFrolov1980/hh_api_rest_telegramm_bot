import requests  # Для запросов по API
import json  # Для обработки полученных результатов
import time  # Для задержки между запросами
import os  # Для работы с файлами
import pprint
import list_with_counter
from hh_functions import get_page,get_requirements, get_sallary


# Собираем требования
requirements = list_with_counter.list_with_counter()

# Собираем зарплаты в валютах
sallaries = list_with_counter.list_with_counter()

# Счетчик не пустых зарплат по каждой валюте
not_zero_sallaries = list_with_counter.list_with_counter()

params = {
    'text': 'NAME:python',  # Текст фильтра. В имени должно быть слово "Аналитик"
    'area': 1,  # Поиск ощуществляется по вакансиям города Москва
    'page': 0,  # Индекс страницы поиска на HH
    'per_page': 100  # Кол-во вакансий на 1 странице
}

concurrent_page = 0
v_pages = 0
vacancies_count = 0

while concurrent_page <= v_pages:

    data = get_page(params, concurrent_page)

    # Преобразуем текст ответа запроса в справочник Python
    jsObj = json.loads(data)
    v_pages = jsObj['pages']
    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    vlst = jsObj['items']

    for vac in vlst:
        vacancies_count += 1
        currency, sallary = get_sallary(vac)
        sallaries.add_item(currency, sallary)
        not_zero_sallaries.add_item(currency)
        requirements.add_items(get_requirements(vac))

    #time.sleep(0.25)
    print('Cтраница: ', concurrent_page + 1, ' из ', v_pages + 1, ' обработана')
    concurrent_page += 1

requirements.sort_by_value()


# Считаем % от требований

#Считаем среднюю ЗП
usd_to_rub = 91.64
eur_to_rub =  98.4

mean_sallary = (sallaries['RUR'] + usd_to_rub*sallaries['USD']+eur_to_rub*sallaries['EUR'])/sum(not_zero_sallaries.list_items.values())

#Собираем большой словарь для записи в json

result = {'params': params,
          'mean_sallary' : mean_sallary,
          'requirements': requirements.calc_percentage().list_items}

#print(result)

with open('data.txt', 'w') as outfile:
    json.dump(result, outfile)