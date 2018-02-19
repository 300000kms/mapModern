import sqlite
'''
este codigo coge todos los fields que contiene la mencion creator o autor o contributor o ilustrator
y entonces alamcena el contenido de todos estos campos para poder hacer un listado que permita conocer todos los autores unicos
dados que esto parte de la extraccion que se realizaó inicial nos encontramos con nombres yuxtapuestos, sobretodo en el campo controbutors
por ello de aqui tendremos que ir hacia el codigo getauthor_op3 para limpiar esto

'''


def getCols(x):
    sql = 'select name from booksfull_fields where name like \'%'+x+'%\''
    fields = sqlite.sql(db, sql)
    af = []
    for f in fields:
        #print f
        af.append(f['name'])
    return af

################################################

db = 'books2.sqlite'
table = 'booksfull'

authors = getCols('author')
creators = getCols('creator')
contri = getCols('contributor')
illus =getCols('illustrator')

sql = ''
for a in authors:
    sql+= 'select %s as autor, \'%s\' as tipo from booksfull ' %(a, 'authors')
    sql += ' union '
for a in creators:
    sql+= 'select %s, \'%s\' from booksfull ' %(a, 'creators')
    sql += ' union '
for a in contri:
    sql+= 'select %s, \'%s\' from booksfull ' %(a, 'contri')
    sql += ' union '
for a in illus:
    sql+= 'select %s, \'%s\' from booksfull ' %(a, 'illus')
    sql += ' union '

sql = sql[0:-6]
print sql
autores = sqlite.sql(db, sql)
sqlite.dict2sqlite('authors2.sqlite', 'authors', autores)




## ahora toca navegar en cada link y buscar su viaf o su denominacion unica para encontrar a los unicos


'''

select schema__Book_author, schema__CreativeWork_author, schema__Person_name
from booksfull

schema__book_creator
schema__creativework_creator

select rowid, schema__book_creator,
schema__creativework_illustrator,
schema__book_illustrator,
schema__creativework_creator,
schema__creativework_contributor,
schema__Book_author, schema__CreativeWork_author, schema__Person_name
from booksfull
where schema__book_creator is null

'''