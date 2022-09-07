# -*- coding: utf-8 -*-
import json
import pprint
import re
from collections import Counter
from os.path import exists
from pickle import dump, load
from pycbrf import ExchangeRates

import requests

def parce(vacancy, pages='3', where='all'):
    url = 'https://api.hh.ru/vacancies'
    # Загрузка текущих курсов ввалют
    rate = ExchangeRates()
    # загрузка файла с цифровым кодом
    if exists('area.txt'):
        with open('area.txt', mode='rb') as f:
            area = load(f)
    else:
        area = {}
    p = {'text': vacancy if where == 'all' else f'NAME: {vacancy}' if where == 'name' else f'COMPANY_NAME: {vacancy}'}
    r = requests.get(url=url, params=p).json()
    # pprint.pprint(r) - успешно
    # количество страниц
    count_pages = r['pages']
    # вывод количества страниц по интересующей вакансии
    # print(count_pages)
    # количество вакансий на странице
    all_count = len(r['items'])
    # print(all_count)
    result = {
        'keywords': vacancy,
        'count': all_count
    }

    # зароботная плата
    sal = {'from': [], 'to': [], 'cur': []}
    # ключеаые навыки
    skillis = []
    # сначала выявляем сколько будет получено страниц
    # и готовим нужные переменные. А затем проходим по каждой из полученных страниц
    for page in range(count_pages):
        if page > int(pages):
            break
        else:
            print(f'Обрабатывается страница {page}')
        # задаем параметры
        p = {'text': vacancy,
             'page': page
             }
        ress = requests.get(url=url, params=p).json()
        all_count = len(ress['items'])
        result['count'] += all_count
        for res in ress['items']:
            # pprint.pprint(res)
            skills = set()
            city_vac = res['area']['name']
    #         добавление города из ответа на запрос, если его нет в файле
            if city_vac not in area:
                area[city_vac] = res['area']['id']
            ar = res['area']
            res_full = requests.get(res['url']).json()
            # pprint.pprint(res_full)
    #         обработка описанеия вакансии
            pp = res_full['description']
            # print(pp)
            pp_re = re.findall(r'\s[A-Za-z-?]+', pp)
            # print(pp_re)
            its = set(x.strip(' -').lower() for x in pp_re)
            # print(its)
            for sk in res_full['key_skills']:
                skillis.append(sk['name'].lower())
                skills.add(sk['name'].lower())
            for it in its:
                if not any(it in x for x in skills):
                    skillis.append(it)
    #окончание формирования списка навыков
    # обработка зарплаты
            if res_full['salary']:
                code = res_full['salary']['currency']
                if rate[code] is None:
                    code = 'RUR'
                k = 1 if code == 'RUR' else float(rate[code].value)
                sal['from'].append(k * res_full['salary']['from']) if res['salary']['from'] else k * res_full['salary']['to']
                sal['to'].append(k * res_full['salary']['to']) if res['salary']['to'] else k * res_full['salary']['from']
    # print(skillis)
    sk2 = Counter(skillis)
    # pprint.pprint(sk2)
    up = sum(sal['from']) / len(sal['from'])
    down = sum(sal['to']) / len(sal['to'])
    result.update(({'down': round(up, 2),
                    'up': round(down, 2)}))
    add = []
    for name, count in sk2.most_common(5):
        add.append({'name': name,
                    'count': count,
                    'percent': round((count / result['count']) * 100, 2)
                    })
    result['requirements'] = add
    with open('area.pkl', 'wb') as f:
        dump(area, f)
    return result


if __name__ == '__main__':
    vacancy = input('Введеите интересующую вакансию: ')
    pprint.pprint(parce(vacancy))







