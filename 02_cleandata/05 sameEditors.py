'''

https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html

https://marcobonzanini.com/2015/02/25/fuzzy-string-matching-in-python/

https://stats.stackexchange.com/questions/123060/clustering-a-long-list-of-strings-words-into-similarity-groups

https://github.com/rieck/harry

https://stackoverflow.com/questions/3329297/finding-groups-of-similar-strings-in-a-large-set-of-strings

https://github.com/doukremt/distance
sudo pip install distance


administracio\u0301n de


imprenta



http://www.karsdorp.io/python-course/



'''

import numpy as np
import sklearn.cluster
import distance
import sqlite

db = 'books2.sqlite'
table = 'booksfull'

rows = sqlite.getRows(db, table, limit=200, fields=['editor'], groupby='editor')
words =[]
for r in rows:
    words.append(str(r).lower().replace('"','')) #convertir el none en str para evitar error

print words
#words = "YOUR WORDS HERE".split(" ") #Replace this line
words = np.asarray(words) #So that indexing with a list will work
lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])

affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.99)
affprop.fit(lev_similarity)
for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join(cluster)
    print(" - *%s:* %s" % (exemplar, cluster_str))