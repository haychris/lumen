import sys
import numpy as np

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN
from sklearn.decomposition import NMF, LatentDirichletAllocation

from process_all_data import get_class_dict, get_course_id_lookup_dict, get_doc_list, get_tfidf_matrix



CLASS_DICT = get_class_dict()
COURSE_ID_LOOKUP_DICT, CLASS_NUMBER_LOOKUP_DICT = get_course_id_lookup_dict(CLASS_DICT)
COURSE_DOC_DICT, DOC_LIST = get_doc_list(CLASS_DICT)
VECTORIZER, X = get_tfidf_matrix(DOC_LIST)


##### K-MEANS #####
K = 12
km = KMeans(n_clusters=K, init='k-means++', max_iter=100, n_init=1)
km.fit(X)

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = VECTORIZER.get_feature_names()

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

tfidf_feature_names = VECTORIZER.get_feature_names()
print_top_words(nmf, tfidf_feature_names, 10)

### LDA model ###
lda = LatentDirichletAllocation(n_topics=K, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=0)
lda.fit(X)
tf_feature_names = VECTORIZER.get_feature_names()
print_top_words(lda, tf_feature_names, 10)

### DBSCAN ###
from sklearn.preprocessing import StandardScaler
X2 = StandardScaler(with_mean=False).fit_transform(X)
db = DBSCAN(eps=0.3, min_samples=2).fit(X)
n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print n_clusters_




############ CREATE RECOMMENDATIONS ############
def load_user_ratings(filename, course_id_lookup, course_doc_dict):
	f = open(filename)
	course_ids = []
	ratings = []
	for line in f:
		department, class_number, rating = line.split()
		course_id_list = course_id_lookup[department + class_number]
		for course in course_id_list:
			course_ids.append(course)
			ratings.append(float(rating))

	
	docs = [course_doc_dict[course_id] for course_id in course_ids]
	return course_ids, ratings, docs

def recommend(vectorizer, trained_clusterer, course_ids, ratings, docs, course_doc_dict):
	trained_clusterer_docs = trained_clusterer.transform(vectorizer.transform(docs))
	cluster_scores = np.zeros(K)
	mean_rating = 3
	for trained_clusterer_doc, rating in zip(trained_clusterer_docs, ratings):
		probs = trained_clusterer_doc / sum(trained_clusterer_doc)
		cluster_scores[:] += (rating-mean_rating)*probs

	trained_clusterer_all_classes = trained_clusterer.transform(vectorizer.transform(course_doc_dict.values()))
	class_ratings = []
	for trained_clusterer_class in trained_clusterer_all_classes:
		class_ratings.append(np.dot(trained_clusterer_class, cluster_scores))


	class_rankings = sorted(list(zip(class_ratings, course_doc_dict.keys())), reverse=True)
	recommendations = []
	for rating, course_id in class_rankings:
		if course_id not in course_ids:
			recommendations.append((course_id, rating))
	return recommendations

COURSE_IDS, RATINGS, DOCS = load_user_ratings('chay_ratings.txt', COURSE_ID_LOOKUP_DICT, COURSE_DOC_DICT)
RECOMMENDATIONS = recommend(VECTORIZER, lda, COURSE_IDS, RATINGS, DOCS, COURSE_DOC_DICT)
print 'Top 20 recommendations:'
for course_id, rating in RECOMMENDATIONS[:20]:
		print CLASS_NUMBER_LOOKUP_DICT[course_id], rating
print 'Bottom 20 recommendations:'
for course_id, rating in RECOMMENDATIONS[-20:]:
		print CLASS_NUMBER_LOOKUP_DICT[course_id], rating