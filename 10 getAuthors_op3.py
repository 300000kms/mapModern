import sqlite

db = 'authors2.sqlite'
table = 'authors'

row = sqlite.sql(db, 'select * from authors')

au=[]
for r in row:
    if r['autor'] is not None:
        autors = r['autor'].split('|')
        for a in autors:
            a.strip(' ')
            a= 'http://'+a
            au.append({'autor':a, 'tipo':r['tipo'], 'name':None})

sqlite.dict2sqlite(db, 'autores_c', au)

'''
--luego ejecutar esto para coger los valores unicos
create table autores_c2 as
SELECT distinct "autor", "tipo", "name"
FROM autores_c
ORDER BY ROWID


--luego
update autores_c2 set name = (select name from a.persons
where persons.id like autores_c2.autor
group by persons.name) limit 100
'''

