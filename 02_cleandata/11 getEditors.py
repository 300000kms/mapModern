import utils
import sqlite


db = 'books2.sqlite'
table = 'booksfull'

'''
editor
placeOfPublication
publication
publisher
'''
cols = utils.getCols('publication')

for c in cols:
    print c

ed = sqlite.sql(db, "select schema__PublicationEvent_type from booksfull where auth like '%cervantes%'")
for e in ed:
    print e