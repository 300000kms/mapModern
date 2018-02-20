# -*- coding: utf-8 -*-
'''
get book data and viaf data

viaf
https://www.oclc.org/developer/develop/web-services/viaf/authority-cluster.en.html

OBJETIVO:
- completar la ficha de libro
- crear un listado de autores únicos asignandoles un id (si existe ya mejor)
- títulos únicos
- detectar reediciones (ediciones únicas)



DEPENDENCIES:

pip install PyLD

'''

import sqlite3
import pprint
import requests
from pyld import jsonld
import json
from lxml import etree


pp = pprint.PrettyPrinter(indent=4)
# la conversion de lis_adv.csv a sqlite ha sido manual
DB= 'db.sqlite'

########################################################################################################################
########################################################################################################################
########################################################################################################################

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getBooksList(id ):
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('''select * from llista1 where rowid >'''+ str(id))
    results = c.fetchall()
    return results

def getDataBook(oclc):
    print 'book :  http://www.worldcat.org/title/fabulas-selectas/oclc/%s' %(oclc)
    url = 'http://experiment.worldcat.org/oclc/%s.jsonld' %(oclc)

    r = requests.get(url)
    #pp.pprint(r.json())

    #js = jsonld.expand(url)
    # pp.pprint ( js )
    # for j in js:
    #     print j['@type'], j.keys()

    return r.text

def biblios(oclc, tt, n=1):
    print 'tt:', tt
    if tt == 'ed':
        url = 'https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=%s&ht=edition&start_holding=%s&serviceCommand=holdingsdata' % (oclc,n)
    elif tt == 'all':
        url = 'https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=%s&start_holding=%s&serviceCommand=holdingsdata' % (oclc,n)
    print url
    r = requests.get(url)
    page = r.text
    tree = etree.HTML(page)
    nbiblios = 0
    nediciones = 0
    if len( tree.xpath('.//*[@class="lib"]') ) > 0:
        #numero biblios
        nb = int(tree.xpath('//*[@class="libsdisplay"]/strong[2]/text()')[0])
        #numero ediciones
        ne = int(tree.xpath('//*[@class="libsdisplay"]/strong[3]/text()')[0].split(' ')[0]) if tree.xpath('//*[@class="libsdisplay"]/strong[3]/text()') else ''
        print nb, ne
        l=[]
        tr = tree.xpath('//*[@class="name"]')
        for t in tr:
            name =  t.xpath('.//*[@class="lib"]/a/text()')[0]
            av = t.xpath('.//*[@class="lib"]/a/@onclick')[0].split(',')[1].replace("'",'') if len(t.xpath('.//*[@class="lib"]/a/@onclick'))>0 else None
            loc =  t.xpath('.//*[@class="geoloc"]/text()')[0]
            l.append([name, av, loc])

        if n+6 >= nb:
            return {'ed':ne, 'nb':nb, 'bib':l }

        else:
            return {'ed':ne, 'nb':nb, 'bib':l+biblios(oclc, tt, n+6)['bib'] }
    else:
        return {'ed': None, 'nb':None, 'bib':[''] }


def saveBookData(id, js, bib_all_bib, bib_all_ne, bib_all_nb, bib_ed_bib, bib_ed_nb):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    #c.execute("update llista1 set description = '%s', bib_all = '%s', bib_ed= '%s' where rowid is %s" %(js, bib_all, bib_ed, id))
    c.execute("update llista1 set description = ?, bib_all_bib = ?, bib_all_ne= ? , bib_all_nb= ? , bib_ed_bib= ? , bib_ed_nb= ? where rowid is ?" , (js, bib_all_bib, bib_all_ne, bib_all_nb, bib_ed_bib, bib_ed_nb, id))
    conn.commit()
    return

def createFields(fields):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    for f in fields:
        try:
            c.execute ('ALTER TABLE llista1 ADD COLUMN %s' %(f))
            conn.commit()
        except Exception as e:
            print e
    conn.close()
    return

def getLastId():
    try:
        with open('logbooks', 'r') as f:
            n = f.read()
    except:
        with open('logbooks', 'w+') as f:
            n = f.read()
    if n == None:
        n = 0
    return n

def saveId(id):
    with open('logbooks', 'w+') as f:
        f.write(str(id))
    return

########################################################################################################################
########################################################################################################################
########################################################################################################################
'''

https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?serviceCommand=spotlightLibrarySearch&oclcnum=912043880&_=1513351180160

https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=431915731&ht=edition&serviceCommand=holdingsdata

https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=431915731&serviceCommand=holdingsdata

https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?wcoclcnum=431915731&ht=edition&serviceCommand=holdingsdata

'''


createFields(['description', 'bib_all_bib', 'bib_all_ne', 'bib_all_nb', 'bib_ed_bib', 'bib_ed_nb'])
#saveId(0)

def scrap():
    id = getLastId()
    books = getBooksList(id)
    t = {}
    for b in books:
        id = str(b['PK_UID'])
        b = str(int(b['oclc']))

        print id, '|', b
        print 1
        js = unicode(getDataBook(b))
        print 2
        bib_all = biblios(b, 'all')
        bib_all_ne = unicode(bib_all['ed'])
        bib_all_nb = unicode(bib_all['nb'])
        bib_all_bib = unicode(bib_all['bib'])
        print 3
        bib_ed  = biblios(b, 'ed')
        bib_ed_nb = unicode(bib_ed['nb'])
        bib_ed_bib = unicode(bib_ed['bib'])

        print 'saving...'
        #for e in  [id, js, bib_all_bib, bib_all_ne, bib_all_nb, bib_ed_bib, bib_ed_nb]:
        #    print e

        saveBookData(id, js, bib_all_bib, bib_all_ne, bib_all_nb, bib_ed_bib, bib_ed_nb)
        saveId(id)
    return


################################################################################################

out =''
while  out != None:
    try:
        scrap()
    except Exception as e:
        print e







