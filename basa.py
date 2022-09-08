import sqlite3

conn = sqlite3.connect('hh.sqlite')


cursor = conn.cursor()

# cursor.execute("insert into region (name)  ('Monty Python and the Holy Grail', 1975, 8.2)")

cursor.execute('select * from region')

result = cursor.fetchall()
print(result)

for item in result:
    print(item)
    print(type(item))

cursor.execute('select * from region where name=?', ('Москва'))
print(cursor.fetchall())