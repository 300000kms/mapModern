# -*- coding: utf-8 -*-
'''
https://platform.worldcat.org/api-explorer/apis

--Retrieve summary classification information based on either ISBN or OCLC Number.
https://platform.worldcat.org/api-explorer/apis/Classify

--consultas mientras se escribe
https://platform.worldcat.org/api-explorer/apis/fastapi

https://platform.worldcat.org/api-explorer/apis/WorldCatDiscoveryAPI

https://github.com/anarchivist/worldcat

1908-1939

'''

import requests
from lxml import etree
import csv
import os
import time

#https://www.worldcat.org/search?
#q=ti%3Aa
#&fq=yr%3A1900..1930+%3E+%3E+x0%3Abook+%3E+mt%3Afic+%3E+ln%3Aspa
#&qt=advanced&dblist=638


#https://www.worldcat.org/search?q=ti%3A&fq=yr%3A1908..1909+%3E+%3E+x0%3Abook+%3E+mt%3Afic+%3E+ln%3Aspa&dblist=638&start=1386&qt=page_number_link

def getUrl(url):
    '''

    :return:
    '''

    headers = {}
    headers['user-agent'] = 'my-app/0.0.1'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'es-ES,es;q=0.8,ca;q=0.6,en;q=0.4,en-US;q=0.2'
    headers['Host'] = 'www.worldcat.org'
    headers['Referer'] = 'http://www.worldcat.org'

    try:
        r = requests.get(url, headers=headers)

    except Exception as e:
        print '>>>', e
        time.sleep(5)
        return getUrl()

    return r

def getPage(p, y1):
    p=str(p)

    url ='https://www.worldcat.org/search?'
    url += 'q=ti%3A'
    url += '&fq=yr%3A'+str(y1)+'..'+str(y1+1)+'+%3E+%3E+x0%3Abook+%3E+mt%3Afic+%3E+ln%3Aspa'
    url += '&dblist=638'
    url += '&start='+p
    url += '&qt=page_number_link'

    print url

    r = getUrl(url)

    page  = r.text
    tree = etree.HTML(page)
    # x = tree.xpath('//*[@class="name"]/a/strong/text()')
    # x = tree.xpath('//*[@class="name"]/a/@href')
    x = tree.xpath('//*[@class="name"]/a')

    results=[]
    for xx in x:
        tit = xx.xpath('strong/text()')[0]
        lnk = 'https://www.worldcat.org'+xx.xpath('@href')[0]
        #print [tit, lnk]
        results.append([tit, lnk])
    print y1, p, len(results)
    #si results es 0 esperar y volver a intentar?? buscar mensaje de error
    return results

def save2csv(l, x, y1):
    with open('list.csv','a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for ll in l:
            writer.writerow([ll[0].encode('utf-8'),ll[1], x, y1])
    return

###############################################################################

def getLog():
    p = 'log'
    if os.path.isfile(p):
        with open(p, 'r+') as f:
            l = f.read()
        if len(l)>0:
            return int(l.split(' ')[0]), int(l.split(' ')[1])
        else:
            return None, None
    else:
        return None, None

def userLog(y, n):
    with open('log', 'w') as f:
        f.write(str(y)+' '+str(n))
    return

def resetLog():
    with open('log', 'w') as f:
        f.write('')
    return
###############################################################################
#lanzar desde 0
#lanzar segun el log
#lanzar segun criterio manual...


yy=1908#1908
nn=1
maxy =1939

#resetLog()

y, n = getLog()

if y == None:
    y = yy
if n==None:
    n=nn

userLog(y, n)
print y,n

while y <= maxy:
    r = getPage(n, y)
    n+=10
    if len(r)  == 0:
        y+=1
        n=1
        print ()
        print ('###############################################################')
    else:
        save2csv(r, n , y)
        userLog(y, n) #esta posicion es buena para tener vacios de datos en los errores


#detectar error por reiteradas queries
#poner al lado los parámetros de busqueda año y num pagina

# https://www.worldcat.org/wcpa/servlet/org.oclc.lac.ui.ajax.ServiceServlet?serviceCommand=spotlightLibrarySearch&oclcnum=798542581
#https://developers.google.com/books/casestudies/