# -*- coding: utf-8 -*-

'''

'''

import json
import sqlite3
import sqlite
import geocoder


#get all biblios
db = 'books2.sqlite'
table = 'booksfull'
fields = ['bib_all_bib', 'bib_all_ne', 'bib_all_nb', 'bib_ed_bib', 'bib_ed_nb']


def getBiblios():
    rows = sqlite.getRows(db, table, fields= fields, limit = 1000)

    bibs = set()

    for r in rows:
        # print 'bib_all_bib', r['bib_all_bib']
        # print 'bib_all_ne',  r['bib_all_ne']
        # print 'bib_all_nb',  r['bib_all_nb']
        # print 'bib_ed_bib',  r['bib_ed_bib']
        # print 'bib_ed_nb',   r['bib_ed_nb']

        bib_all_bib = eval(r['bib_all_bib']) if type(eval(r['bib_all_bib'])) is list else []
        bib_ed_bib  = eval(r['bib_ed_bib'])  if type(eval(r['bib_ed_bib']))  is list else []

        # print len(bib_all_bib), bib_all_bib
        # print len(bib_ed_bib), bib_ed_bib

        for b in bib_all_bib:
            bibs.add(tuple(b))
        for b in bib_ed_bib:
            bibs.add(tuple(b))

    biblios = []
    for b in bibs:
        if len(b) >= 3:
            biblios.append( {'library': b[0], 'siglas':b[1], 'address':b[2]})

    sqlite.dict2sqlite('libraries.sqlite', 'libraries', biblios)
    return

def geolocate(db, table, rows):
    nrows = len(sqlite.getRows(db, table, fields=None))
    print nrows
    for r in range(1,nrows+1):
        row = sqlite.getRow(db, table, id=r)
        if row['lat'] == None:

            g = geocoder.arcgis(row['address'])
            pos = g.latlng
            if pos != None:
                sqlite.update(db, table, {'lat':pos[0], 'lng': pos[1]}, {'ROWID':r})
            else:
                print row['address']
    return


#getBiblios()

sqlite.addColumns('libraries.sqlite', 'libraries', ['lat', 'lng'])

geolocate('libraries.sqlite', 'libraries', 'f')