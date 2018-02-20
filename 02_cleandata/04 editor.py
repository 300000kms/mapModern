# -*- coding: utf-8 -*-

'''

'''

import sqlite3
import sqlite
import geocoder
import re

db = 'books2.sqlite'
table = 'booksfull'

sqlite.addColumns(db, table, ['city', 'editor', 'editor_year'])
rows = sqlite.getRows(db, table, fields=['ROWID', 'pub', 'city'])

results =[]
for r in rows:
    if type(r['pub']) is unicode and ':' in r['pub']:# and r['city'] is None:
        result = {}
        print
        #print r

        city =  r['pub'].split(':')[0]
        city = city.strip(' []')
        city = city.split('[')[0].strip(' ').strip('?').replace("'",'')
        result['city']=city

        ed = r['pub'].split(':')[1].split(',')[0].strip(' ').replace("'",'')
        result['editor']=ed

        year = re.findall(r'\d\d\d\d', r['pub'])
        year = year[0] if len(year)>0 else None
        result['editor_year']=year

        results.append(result)

        sqlite.update(db, table, results, {'ROWID': r['rowid']})
        results =[]

        # print r['pub']
        # print city
        # print ed
        # print year
        # print
        #print '.'

print 'done!'

'''
after sql

update booksfull set editor = replace(editor, '[', '')
where editor like '%[%'


update booksfull set editor = replace(editor, ']', '')
where editor like '%]%'

select  editor, count() as c from booksfull group by editor order by c desc


'''
    # ciudad
    # editorial
    # año


