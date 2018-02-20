'''
tomar el json
coger los campos unicos
montar db
volcar

montar listado excel de los campos para poder anotar

verificar
- campo de autor/traducor/ilustrador (type)
- buscar un ejemplo de libro con coautor, traductor e ilustrador
-


'''

import json
import sqlite3


def getAllFields(js):
    fields = set([])
    for j in js:
        fields.update(j.keys())
    result = list(fields)
    return result


def createDb(fields, db = 'books.sqlite'):
    fields.sort()
    fields = [f.replace(':', '__').replace('@','') for f in fields]
    conn = sqlite3.connect(db)
    c = conn.cursor()
    fi = ', '.join(fields)

    sql = 'create table books(%s)' %(fi)
    print sql
    c.execute(sql)
    conn.commit()
    return


def volcar(js, db = 'books.sqlite'):
    '''
    '''
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for j in js:
        keys = ','.join(j.keys()).replace(':', '__').replace('@','')
        val = ["'"+jj.replace('http://', '').replace('@','').replace("'","''").replace(':','__')+"'" for jj in j.values()]
        values = ', '.join(val)
        sql = 'insert into books(%s) values(%s)' %(keys , values)
        #print sql
        c.execute(sql)
    conn.commit()
    return


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
##lee el txt rascado de la web
js = json.load(open('books.txt', 'r'))
print 'opened'

#######################################################################################################################
##coje todos los campos de los distintos diccionarios
fields = getAllFields(js)
fields.sort()

##guarda un listado de los fields
print 'i have the fields'
with open('fields.csv', 'w') as f:
    for fi in fields:
        f.write(fi+'\n')

#guarda los datos..
createDb(fields, db = 'books2.sqlite')
print 'db done'

volcar(js, db = 'books2.sqlite')
print 'volcado!'