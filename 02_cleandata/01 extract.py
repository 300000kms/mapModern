# -*- coding: utf-8 -*-

'''

lee la db
-read the db

bib_all : listado biblios donde está la obra
bib_ed : listado biblios donde esta la edicion
bib_all_ne : numero de ediciones
bib_all_nb : numero de bibliotecas donde esta
bib_ed_nb : numero de biblios de esta edicion
bib_ed_bib : listado de biblios de esta edicion

registros 58114

debemos tener unos 28 types escaneado el 40% de la db
232-383

con el 60% de la db tenemos 395 subtypes, 386 si excluimos le origen de meta

montar diccionario de types con características
en el casode locativos podemos agregar valores
en el caso de autores hay que poder diferenciar?
mirar si autor va acompañado del tipo de autor (ilustrador, traductor)

'''
import json
import sqlite3
import sqlite



def dict_factory(cursor, row):
    d ={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getRow(x):
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    c = conn.cursor()
    sql = '''select * from llista1 where ROWID = %s''' %(x)
    c. execute(sql)
    result = c.fetchone()
    return result


def flat(b):
    if type(b) is list:
        r = []
        for bb in b:
            if type(bb) is list:
                r.append(flat(bb))
            else:
                r.append(str(bb))
        result= ' | '.join(list(set(r)))
    elif b is None:
        result = ''
    else:
        result = str(b)
    return result


def getCity(s):
    '''
    si tiene soble punto pillo lo que le precede
    sino pillo lo que precede la primera coma
    '''
    if ':' in s:
        r = s.split(':')[0].strip(' ')
    elif ',' in s:
        #ojo, a veces ahay dos ciudades seguidas por comas y otras hay ciudad y país...como???
        r = s.split(',')[0].strip(' ')
    else:
        r = '>>>>'+s
    return r



def getEd(s):
    '''
    si tiene soble punto pillo lo que le precede
    sino pillo lo que precede la primera coma
    '''
    if ':' in s:
        r = ' '.join(s.split(':')[1:])
    elif ',' in s:
        r = ' '.join(s.split(',')[1:])
    else:
        r = '>>>>'+s
    return r


#####################################################################
#####################################################################
#####################################################################


def extractData():
    rows = sqlite.getRows(DB, 'llista1', limit=None)
    for row in rows:
        row = getRow(x)
        #city = getCity(row['pub'])
        #ed = getEd(row['pub'])
        try:
            print row['bib_all']
            print row['bib_ed_bib']
            print row['bib_ed']
            print row['bib_all']
        except:
            print '---------------------------------'
        print

def save2csv(l, file = 'list_adv.csv'):
    file = 'list_adv.csv'
    file_exists = os.path.isfile(file)
    # l = flatten2csv(l)
    keys = sorted(l[0].keys())

    with open(file, 'a') as f:
        w = csv.DictWriter(f, keys, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        # writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        if not file_exists:
            w.writeheader()

        for ll in l:
            ll = flatten2csv(ll)
            w.writerow(ll)
    return

def getAllFields(js):
    print js
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
    try:
        c.execute(sql)
    except Exception as e:
        print e
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

#####################################################################
#####################################################################
#####################################################################

DB = 'db.sqlite'

books    = []
types    = []
subtypes = []

rows = sqlite.getRows(DB, 'llista1', limit=None )
for row in rows:
    book={}
    book['oclc']=str(int(row['oclc']))

    try:
        graph = eval(row['description'])['@graph']

        for id in graph:
            if type(id.get('@type')) is list:
                for t in id.get('@type'):
                    types.append(t)
                    for i in id:
                        tt = t+'_'+i
                        subtypes.append(tt)
                        if book.get(tt) is None:
                            book[tt] = [id[i]]
                        else:
                            book[tt] = book[tt]+[id[i]]
            else:
                types.append(id.get('@type'))
                if id.get('@type') != None:
                    for i in id:
                        tt = '%s_%s' %(id.get('@type'), i)
                        subtypes.append(tt)
                        if book.get(tt) is None:
                            book[tt] = [id[i]]
                        else:
                            book[tt] = book[tt]+[id[i]]

        #aplanar book values!
        for b in book:
            book[b]=flat(book[b])

        books.append(book)
        print '.'
    except Exception as e:
        print e
        #print row['description']



##get unique
books = {v['oclc']:v for v in books}.values()

#####
fields = getAllFields(books)
fields.sort()

##guarda un listado de los fields
print 'i have the fields'
with open('fields.csv', 'w') as f:
    for fi in fields:
        f.write(fi+'\n')


createDb(fields, db = 'books2.sqlite')
print 'db done'


volcar(books, db = 'books2.sqlite')
print 'volcado!'


print len(types)
ts =set(types)
print len(ts)
print ts

print len(subtypes)
sts =set(subtypes)
print len(sts)
print sts

'''
create table booksfull as
SELECT a.*, "bgn__Agent_id", "bgn__Agent_type", "bgn__Agent_name", "bgn__CD_id", "bgn__CD_type", "bgn__CD_bookFormat", "bgn__CD_contributor", "bgn__CD_datePublished", "bgn__CD_describedby", "bgn__CD_exampleOfWork", "bgn__CD_genre", "bgn__CD_inLanguage", "bgn__CD_isPartOf", "bgn__CD_name", "bgn__CD_oclcnum", "bgn__CD_placeOfPublication", "bgn__CD_productID", "bgn__CD_publication", "bgn__CD_publisher", "bgn__Meeting_id", "bgn__Meeting_type", "bgn__Meeting_location", "bgn__Meeting_name", "bgn__Microform_id", "bgn__Microform_type", "bgn__Microform_about", "bgn__Microform_alternateName", "bgn__Microform_audience", "bgn__Microform_author", "bgn__Microform_bookEdition", "bgn__Microform_comment", "bgn__Microform_contributor", "bgn__Microform_copyrightYear", "bgn__Microform_creator", "bgn__Microform_datePublished", "bgn__Microform_describedby", "bgn__Microform_description", "bgn__Microform_editor", "bgn__Microform_exampleOfWork", "bgn__Microform_genre", "bgn__Microform_hasPart", "bgn__Microform_inLanguage", "bgn__Microform_isPartOf", "bgn__Microform_isSimilarTo", "bgn__Microform_name", "bgn__Microform_numberOfPages", "bgn__Microform_oclcnum", "bgn__Microform_placeOfPublication", "bgn__Microform_productID", "bgn__Microform_publication", "bgn__Microform_publisher", "bgn__Microform_seeAlso", "bgn__Microform_translationOfWork", "bgn__Microform_workExample", "bgn__MusicScore_id", "bgn__MusicScore_type", "bgn__MusicScore_about", "bgn__MusicScore_creator", "bgn__MusicScore_datePublished", "bgn__MusicScore_describedby", "bgn__MusicScore_exampleOfWork", "bgn__MusicScore_inLanguage", "bgn__MusicScore_isPartOf", "bgn__MusicScore_isSimilarTo", "bgn__MusicScore_name", "bgn__MusicScore_oclcnum", "bgn__MusicScore_placeOfPublication", "bgn__MusicScore_productID", "bgn__MusicScore_publication", "bgn__MusicScore_publisher", "bgn__Newspaper_id", "bgn__Newspaper_type", "bgn__Newspaper_datePublished", "bgn__Newspaper_describedby", "bgn__Newspaper_exampleOfWork", "bgn__Newspaper_inLanguage", "bgn__Newspaper_name", "bgn__Newspaper_oclcnum", "bgn__Newspaper_placeOfPublication", "bgn__Newspaper_productID", "bgn__Newspaper_publication", "bgn__Newspaper_publisher", "bgn__PublicationSeries_id", "bgn__PublicationSeries_type", "bgn__PublicationSeries_creator", "bgn__PublicationSeries_hasPart", "bgn__PublicationSeries_issn", "bgn__PublicationSeries_label", "bgn__PublicationSeries_name", "bgn__Thesis_id", "bgn__Thesis_type", "bgn__Thesis_about", "bgn__Thesis_alternateName", "bgn__Thesis_contributor", "bgn__Thesis_creator", "bgn__Thesis_datePublished", "bgn__Thesis_describedby", "bgn__Thesis_editor", "bgn__Thesis_exampleOfWork", "bgn__Thesis_genre", "bgn__Thesis_inLanguage", "bgn__Thesis_inSupportOf", "bgn__Thesis_isPartOf", "bgn__Thesis_isSimilarTo", "bgn__Thesis_name", "bgn__Thesis_numberOfPages", "bgn__Thesis_oclcnum", "bgn__Thesis_placeOfPublication", "bgn__Thesis_productID", "bgn__Thesis_publication", "bgn__Thesis_publisher", "bgn__Thesis_seeAlso", "bgn__Thesis_url", "genont__ContentTypeGenericResource_id", "genont__ContentTypeGenericResource_type", "genont__ContentTypeGenericResource_about", "genont__ContentTypeGenericResource_dateModified", "genont__ContentTypeGenericResource_inDataset", "genont__InformationResource_id", "genont__InformationResource_type", "genont__InformationResource_about", "genont__InformationResource_dateModified", "genont__InformationResource_inDataset", "pto__Manuscript_id", "pto__Manuscript_type", "pto__Manuscript_about", "pto__Manuscript_alternateName", "pto__Manuscript_audience", "pto__Manuscript_author", "pto__Manuscript_bookFormat", "pto__Manuscript_comment", "pto__Manuscript_contributor", "pto__Manuscript_copyrightYear", "pto__Manuscript_creator", "pto__Manuscript_datePublished", "pto__Manuscript_describedby", "pto__Manuscript_description", "pto__Manuscript_exampleOfWork", "pto__Manuscript_genre", "pto__Manuscript_inLanguage", "pto__Manuscript_inSupportOf", "pto__Manuscript_isPartOf", "pto__Manuscript_isSimilarTo", "pto__Manuscript_name", "pto__Manuscript_numberOfPages", "pto__Manuscript_oclcnum", "pto__Manuscript_placeOfPublication", "pto__Manuscript_productID", "pto__Manuscript_publication", "pto__Manuscript_publisher", "pto__Manuscript_seeAlso", "pto__Manuscript_url", "pto__Web_document_id", "pto__Web_document_type", "pto__Web_document_about", "pto__Web_document_creator", "pto__Web_document_datePublished", "pto__Web_document_describedby", "pto__Web_document_editor", "pto__Web_document_exampleOfWork", "pto__Web_document_genre", "pto__Web_document_inLanguage", "pto__Web_document_inSupportOf", "pto__Web_document_isSimilarTo", "pto__Web_document_name", "pto__Web_document_oclcnum", "pto__Web_document_placeOfPublication", "pto__Web_document_productID", "pto__Web_document_publication", "pto__Web_document_seeAlso", "pto__Web_document_url", "schema__Book_id", "schema__Book_type", "schema__Book_about", "schema__Book_alternateName", "schema__Book_audience", "schema__Book_author", "schema__Book_awards", "schema__Book_bookEdition", "schema__Book_bookFormat", "schema__Book_comment", "schema__Book_contentRating", "schema__Book_contributor", "schema__Book_copyrightYear", "schema__Book_creator", "schema__Book_datePublished", "schema__Book_describedby", "schema__Book_description", "schema__Book_editor", "schema__Book_exampleOfWork", "schema__Book_genre", "schema__Book_hasPart", "schema__Book_illustrator", "schema__Book_inLanguage", "schema__Book_inSupportOf", "schema__Book_isPartOf", "schema__Book_isSimilarTo", "schema__Book_label", "schema__Book_name", "schema__Book_numberOfPages", "schema__Book_oclcnum", "schema__Book_placeOfPublication", "schema__Book_productID", "schema__Book_publication", "schema__Book_publisher", "schema__Book_seeAlso", "schema__Book_translationOfWork", "schema__Book_url", "schema__Book_workExample", "schema__CreativeWork_id", "schema__CreativeWork_type", "schema__CreativeWork_about", "schema__CreativeWork_alternateName", "schema__CreativeWork_audience", "schema__CreativeWork_author", "schema__CreativeWork_awards", "schema__CreativeWork_bookEdition", "schema__CreativeWork_bookFormat", "schema__CreativeWork_comment", "schema__CreativeWork_contentRating", "schema__CreativeWork_contributor", "schema__CreativeWork_copyrightYear", "schema__CreativeWork_creator", "schema__CreativeWork_datePublished", "schema__CreativeWork_describedby", "schema__CreativeWork_description", "schema__CreativeWork_editor", "schema__CreativeWork_exampleOfWork", "schema__CreativeWork_genre", "schema__CreativeWork_hasPart", "schema__CreativeWork_illustrator", "schema__CreativeWork_inLanguage", "schema__CreativeWork_inSupportOf", "schema__CreativeWork_isPartOf", "schema__CreativeWork_isSimilarTo", "schema__CreativeWork_label", "schema__CreativeWork_language", "schema__CreativeWork_name", "schema__CreativeWork_numberOfPages", "schema__CreativeWork_oclcnum", "schema__CreativeWork_placeOfPublication", "schema__CreativeWork_productID", "schema__CreativeWork_publication", "schema__CreativeWork_publisher", "schema__CreativeWork_seeAlso", "schema__CreativeWork_translationOfWork", "schema__CreativeWork_url", "schema__CreativeWork_workExample", "schema__Event_id", "schema__Event_type", "schema__Event_location", "schema__Event_name", "schema__IndividualProduct_id", "schema__IndividualProduct_type", "schema__IndividualProduct_about", "schema__IndividualProduct_alternateName", "schema__IndividualProduct_audience", "schema__IndividualProduct_author", "schema__IndividualProduct_bookFormat", "schema__IndividualProduct_comment", "schema__IndividualProduct_contributor", "schema__IndividualProduct_copyrightYear", "schema__IndividualProduct_creator", "schema__IndividualProduct_datePublished", "schema__IndividualProduct_describedby", "schema__IndividualProduct_description", "schema__IndividualProduct_exampleOfWork", "schema__IndividualProduct_genre", "schema__IndividualProduct_inLanguage", "schema__IndividualProduct_inSupportOf", "schema__IndividualProduct_isPartOf", "schema__IndividualProduct_isSimilarTo", "schema__IndividualProduct_name", "schema__IndividualProduct_numberOfPages", "schema__IndividualProduct_oclcnum", "schema__IndividualProduct_placeOfPublication", "schema__IndividualProduct_productID", "schema__IndividualProduct_publication", "schema__IndividualProduct_publisher", "schema__IndividualProduct_seeAlso", "schema__IndividualProduct_url", "schema__Intangible_id", "schema__Intangible_type", "schema__Intangible_hasPart", "schema__Intangible_name", "schema__Intangible_seeAlso", "schema__MediaObject_id", "schema__MediaObject_type", "schema__MediaObject_about", "schema__MediaObject_alternateName", "schema__MediaObject_audience", "schema__MediaObject_author", "schema__MediaObject_bookEdition", "schema__MediaObject_bookFormat", "schema__MediaObject_comment", "schema__MediaObject_contributor", "schema__MediaObject_copyrightYear", "schema__MediaObject_creator", "schema__MediaObject_datePublished", "schema__MediaObject_describedby", "schema__MediaObject_description", "schema__MediaObject_editor", "schema__MediaObject_exampleOfWork", "schema__MediaObject_genre", "schema__MediaObject_hasPart", "schema__MediaObject_illustrator", "schema__MediaObject_inLanguage", "schema__MediaObject_inSupportOf", "schema__MediaObject_isPartOf", "schema__MediaObject_isSimilarTo", "schema__MediaObject_name", "schema__MediaObject_oclcnum", "schema__MediaObject_placeOfPublication", "schema__MediaObject_productID", "schema__MediaObject_publication", "schema__MediaObject_publisher", "schema__MediaObject_seeAlso", "schema__MediaObject_translationOfWork", "schema__MediaObject_url", "schema__Organization_id", "schema__Organization_type", "schema__Organization_name", "schema__PeopleAudience_id", "schema__PeopleAudience_type", "schema__PeopleAudience_audienceType", "schema__Periodical_id", "schema__Periodical_type", "schema__Periodical_about", "schema__Periodical_creator", "schema__Periodical_datePublished", "schema__Periodical_describedby", "schema__Periodical_exampleOfWork", "schema__Periodical_genre", "schema__Periodical_inLanguage", "schema__Periodical_isSimilarTo", "schema__Periodical_name", "schema__Periodical_oclcnum", "schema__Periodical_placeOfPublication", "schema__Periodical_productID", "schema__Periodical_publication", "schema__Periodical_publisher", "schema__Person_id", "schema__Person_type", "schema__Person_birthDate", "schema__Person_deathDate", "schema__Person_familyName", "schema__Person_givenName", "schema__Person_name", "schema__Place_id", "schema__Place_type", "schema__Place_identifier", "schema__Place_name", "schema__ProductModel_id", "schema__ProductModel_type", "schema__ProductModel_isbn", "schema__PublicationEvent_id", "schema__PublicationEvent_type", "schema__PublicationEvent_location", "schema__PublicationEvent_organizer", "schema__PublicationEvent_startDate", "schema__Thing_id", "schema__Thing_type", "schema__Thing_name"
FROM "books" as b, (select * from a.llista1 group by oclc) as a
where cast(b.oclc as int)= a.oclc

'''