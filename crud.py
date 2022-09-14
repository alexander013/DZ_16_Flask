from sqlite3 import connect
from BAZA_18 import Session, Words, Skills, Wordskill


def add_words(cur, new):
    """
    Добавление или редактирование строки в таблице со строками поиска.
    :param cur: передача курсора доступа к базе данных.
    :param new: словарь с данными.
    :return: Курсор доступа к базе
    """
    # cur.execute('select * from words where words.word = ?', (new['keywords'],))
    # res = cur.fetchone()
    res = cur.query(Words).filter_by(word=new['keywords']).first()
    print(res)
    if res:
        if res.count < new['count']:
            res.count = new['count']
            res.up = new['up']
            res.down = new['down']
        # if res[2] < new['count']:
        #     # обновление строки таблицы
        #     cur.execute('update words set count = ?, up = ?, down = ? where words.id = ?',
        #                 (new['count'], new['up'], new['down'], res[0]))
            print('Edit')
        else:
            print('Not edit')
    else:
        # добавление строки в таблице
        # cur.execute('insert into words values (null, ?, ?, ?, ?)',
        #             (new['keywords'], new['count'], new['up'], new['down']))
        cur.add(Words(word=new['keywords'], count=new['count'], up=new['up'], down=new['down']))
        print('Done')
    return cur


def add_skills(cur, new):
    """
    Добавление строки в таблицу навыков.
    :param cur: объект курсора доступа к базе данных.
    :param new: словарь данных с результатами обработки.
    :return: курсор доступа к базе данных.
    """
    for item in new['requirements']:
        # res = cur.execute('select * from skills where skills.name = ?', (item['name'],))
        res = cur.query(Skills).filter_by(name=item['name']).one_or_none()
        if not res:
            print(item['name'])
            cur.add(Skills(name=item['name']))
        else:
            print('skill not added')
    return cur


# def add_ws(cur, new):
#     """
#     Добавление строки в сводную таблицу
#     :param cur: курсор доступа к базе данных.
#     :param new: словарь с данными обработки вакансий.
#     :return: курсор доступа к базе данных.
#     """
#     cur.execute('select id, count from words where words.word = ?', (new['keywords'],))
#     word_id, word_count = cur.fetchone()
#     for item in new['requirements']:
#         cur.execute('select id from skills where skills.name = ?', (item['name'],))
#         skill_id = cur.fetchone()[0]
#         print(word_id, skill_id)
#         cur.execute('select * from wordskills as ws where ws.id_word = ? and ws.id_skill = ?',
#                     (word_id, skill_id))
#         res = cur.fetchone()
#         if not res:
#             cur.execute('insert into wordskills values (null, ?, ?, ?, ?)',
#                         (word_id, skill_id, item['count'], item['percent']))
#             print('ws done')
#         elif word_count < new['count']:
#             cur.execute('update wordskills as ws set count = ?, percent = ? where ws.id_word = ? and ws.id_skill = ?',
#                         (item['count'], item['percent'], word_id, skill_id))
#             print('ws edit')
#         print('ws not edit')
#     return cur

def add_ws(cur, new):
    res = cur.query(Words).filter_by(word=new['keywords']).first()
    word_id, word_count = res.id, res.count
    for item in new['requirements']:
        skill_id = cur.query(Skills).filter_by(name=item['name']).first().id
        print(word_id, skill_id)
        res = cur.query(Wordskill).filter_by(id_word=word_id, id_skill=skill_id).one_or_none()
        if not res:
            cur.add(Wordskill(id_word=word_id, id_skill=skill_id, count=item['count'], percent=item['percent']))
            print('ws done')
        elif word_count < new['count']:
            res.count = item['count']
            res.percent = item['percent']
            print('ws edit')
        else:
            print('ws not edit')
    return cur


# def add_row(new):
#     """
#     Добавление строк в таблицы.
#     :param new: словарь с результатами обработки вакансий
#     """
#     con = connect('base.sqlite')
#     cur = con.cursor()
#     cur = add_words(cur, new)
#     cur = add_skills(cur, new)
#     cur = add_ws(cur, new)
#     con.commit()
#     con.close()

def add_row(new):
    cur = Session()
    cur = add_words(cur, new)
    cur = add_skills(cur, new)
    cur = add_ws(cur, new)
    cur.commit()
    cur.close()

if __name__ == '__main__':
    add_row({'keywords': 'python1', 'count': 225, 'up': 234567.32, 'down': 654321.34,
             'requirements': [{'name': 'first', 'count': 25, 'percent': 34},
                              {'name': 'second', 'count': 24, 'percent': 33}]})