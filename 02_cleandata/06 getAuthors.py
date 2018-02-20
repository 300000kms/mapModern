import sqlite

db = 'books2.sqlite'
table = 'booksfull'

rows = sqlite.getRows(db, table, limit=None, fields=['schema__Person_name'], groupby='schema__Person_name')

names =set([])
for n, r in enumerate(rows):
    i=1
    if r['schema__Person_name'] is not None:
        for rr in r['schema__Person_name'].split('|'):
            names.add(rr.strip(' ').lower())
    else:
        print i
        i+=1


print len(names)
#12976
adicts = []
for n in list(names):
    adicts.append({'author':n})

sqlite.dict2sqlite('authors.sqlite', 'authors', adicts)

'''
update authors
set books = (select count() from (select PK_UID from booksfull where schema__Person_name like '%'||author||'%') as a)
'''

