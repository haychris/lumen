import sys
import numpy as np

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN
from sklearn.decomposition import NMF, LatentDirichletAllocation

from process_all_data import get_class_dict, get_doc_list, get_tfidf_matrix



CLASS_DICT = get_class_dict()
DOC_LIST = get_doc_list(CLASS_DICT)
vectorizer, X = get_tfidf_matrix(DOC_LIST)


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
g = open(sys.argv[1])
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