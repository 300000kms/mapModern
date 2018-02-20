import sqlite

db = 'books2.sqlite'
table = 'booksfull'

sql = 'select name from booksfull_fields where name like \'%schema%\''
fields = sqlite.sql(db, sql)

af = []
for f in fields:
    af.append(f['name'])

sql = 'select %s  from booksfull' %(', '.join(af))

print sql