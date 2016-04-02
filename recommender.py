from __future__ import print_function

import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pandas as pd

from sklearn.cluster import KMeans

feature_df = pd.read_csv(sys.argv[1])

f = open(sys.argv[1])
header = f.readline()
doc_list = f.read().replace('"', '').replace(',', ' ').split('\n')

vectorizer = TfidfVectorizer(input='content', max_df=0.5, stop_words='english', use_idf=True)
X = vectorizer.fit_transform(doc_list)

# counter = CountVectorizer(input='content')
# count_matrix = counter.fit_transform(doc_list)

# tfidf_transform = TfidfTransformer()
# tfidf_transform.fit(count_matrix)
# tfidf_matrix = tfidf_transform.transform(count_matrix)


# X = tfidf_matrix
K = 9
km = KMeans(n_clusters=K, init='k-means++', max_iter=100, n_init=1)
km.fit(X)

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

for i in range(K):
	print("Cluster %d:" % i, end='')
	for ind in order_centroids[i, :10]:
		print(' %s' % terms[ind], end='')
	print()