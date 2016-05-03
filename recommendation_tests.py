import sys
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN
from sklearn.decomposition import NMF, LatentDirichletAllocation
"""
Takes in *_features.csv as input, outputs
"""


feature_df = pd.read_csv(sys.argv[1])
doc_list = open(sys.argv[1]).read().replace('"', '').replace(',', ' ').split('\n')


"""
Creates dictionary where class name is the key (ex: "ORF 350"). 
Value is a cleaned version of the line in the csv.
"""
f = open(sys.argv[1])
header = f.readline()
column_keys = header.split(',')
class_key = 'all_listings_string'
class_key_col_num = column_keys.index(class_key)

class_dict = defaultdict(str)
cleaned_class_dict = defaultdict(str)
for line in f:
	split = line.split(',')
	class_listing = split[class_key_col_num].replace('"', '')
	# Since a class can go under multiple class names (ELE 206 COS 306), add each class separately as a key
	classes = class_listing.split()
	for i in range(0,len(classes), 2):
		class_dict[classes[i] + classes[i+1]] = line
		cleaned_class_dict[classes[i] + classes[i+1]] = line.replace('"', '').replace(',', ' ')


"""
Creates a Tfidf matrix of word counts per document. 
Uses english stop words. 
Word must appear in at least 2 docs, and no more than 50 percent of all docs in order to be included.
"""
vectorizer = TfidfVectorizer(input='content', max_df=0.5, stop_words='english', use_idf=True, min_df=2)
vectorizer.fit(doc_list)
X = vectorizer.transform(doc_list)

# counter = CountVectorizer(input='content')
# count_matrix = counter.fit_transform(doc_list)

# tfidf_transform = TfidfTransformer()
# tfidf_transform.fit(count_matrix)
# tfidf_matrix = tfidf_transform.transform(count_matrix)
# X = tfidf_matrix

##### K-MEANS #####
K = 12
km = KMeans(n_clusters=K, init='k-means++', max_iter=100, n_init=1)
km.fit(X)

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

for i in range(K):
	print "Cluster %d:" % i,
	for ind in order_centroids[i, :10]:
		print terms[ind],
	print

##### SOFT CLUSTERING #####
# ap = AffinityPropagation()
# ap.fit(X)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic #%d:" % topic_idx,
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]) 
    print

### NMF model ###
nmf = NMF(n_components=K, random_state=1, alpha=.1, l1_ratio=.5).fit(X)

tfidf_feature_names = vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, 10)

### LDA model ###
lda = LatentDirichletAllocation(n_topics=K, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=0)
lda.fit(X)
tf_feature_names = vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 10)

### DBSCAN ###
from sklearn.preprocessing import StandardScaler
X2 = StandardScaler(with_mean=False).fit_transform(X)
db = DBSCAN(eps=0.3, min_samples=2).fit(X)
n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print n_clusters_




############ CREATE RECOMMENDATIONS ############
g = open(sys.argv[2])
docs = []
ratings = []
for line in g:
	the_class, rating = line.split()
	doc = cleaned_class_dict[the_class]
	if doc is not '':
		docs.append(doc)
		ratings.append(float(rating))

lda_docs = lda.transform(vectorizer.transform(docs))
cluster_scores = np.zeros(K)
mean_rating = 3
for lda_doc, rating in zip(lda_docs, ratings):
	probs = lda_doc / sum(lda_doc)
	cluster_scores[:] += (rating-mean_rating)*probs

lda_all_classes = lda.transform(vectorizer.transform(cleaned_class_dict.values()))
class_ratings = []
for lda_class in lda_all_classes:
	class_ratings.append(np.dot(lda_class, cluster_scores))


class_rankings = sorted(list(zip(class_ratings, cleaned_class_dict.keys())), reverse=True)
for rating, class_name in class_rankings[:20] + class_rankings[-20:]:
	print class_name, rating
