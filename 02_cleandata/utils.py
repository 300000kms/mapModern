import sqlite




def getCols(x):
    db = 'books2.sqlite'
    table = 'booksfull'
    '''selecciona las columnas ocn uncontenido x'''
    sql = 'select name from booksfull_fields where name like \'%'+x+'%\''
    fields = sqlite.sql(db, sql)
    af = []
    for f in fields:
        #print f
        af.append(f['name'])
    return af