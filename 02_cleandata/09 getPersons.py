# -*- coding: utf-8 -*-
import sqlite

db = 'books2.sqlite'
table = 'booksfull'

def getLargest(l):
    m =[]
    for ll in l:
        m.append(len(ll))
    mm = max(m)
    i =m.index(mm)
    return l[i]


def gfd(d):
    m =[]
    for dd in d:
        print dd
        if dd['@language'] == 'en':
            return dd['@value']


books = sqlite.sql(db, 'select rowid, description as d from booksfull')
authors = []
for b in books:
    row = b['rowid']
    print row
    if b['d'][0:6] !='<html>':
        des= eval(b['d'])

        for d in des['@graph']:
            #print d
            if d.get('@type') == 'schema:Person':
                d['id'] = d.pop('@id')
                d['type'] = d.pop('@type')
                for dd in d:
                    if type(d[dd]) is list:
                        if type(d[dd][0]) is dict:
                            print d[dd]
                            d[dd] = gfd(d[dd]).decode('utf-8')
                            print d[dd]
                        else:
                            print d[dd]
                            d[dd] = getLargest(d[dd]).decode('utf-8')
                            print d[dd]
                    else:
                        d[dd] = d[dd].decode('utf-8')
                d['row'] = row
                authors.append(d)


##
sqlite.dict2sqlite('persons.sqlite', 'persons', authors)

'''
--
SELECT ROWID, count() as c, min("birthDate"), max("birthDate"), min("deathDate"),max("deathDate"), "familyName", "givenName",max("id"), "name", "row", "type"
FROM "authors"
group by name
order by name desc

--analisis con pseudonimo
SELECT ROW, count() as c, min("birthDate"), max("birthDate"), min("deathDate"),max("deathDate"), "familyName", "givenName",max("id"), "name", "row", "type"
FROM "authors"
where row in (select row from authors where name like '%seud%')
group by name
order by row desc
'''


