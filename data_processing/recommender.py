import sys
import numpy as np

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN
from sklearn.decomposition import NMF, LatentDirichletAllocation

from process_all_data import get_all

CLASS_DICT, COURSE_ID_LOOKUP_DICT, CLASS_NUMBER_LOOKUP_DICT, COURSE_DOC_DICT, DOC_LIST, VECTORIZER, X = get_all(
    'recommender_data.pickle', False)
print 'Finished retrieving data'

##### K-MEANS #####
K = 50


def get_kmeans(dat_matrix, vectorizer):
    km = KMeans(n_clusters=K, init='k-means++', max_iter=300, n_init=20)
    km.fit(dat_matrix)

    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    for i in range(K):
        print "Cluster %d:" % i,
        for ind in order_centroids[i, :10]:
            print terms[ind],
        print
    return km


##### SOFT CLUSTERING #####
# ap = AffinityPropagation()
# ap.fit(X)


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic #%d:" % topic_idx,
        print " ".join(
            [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    print


### NMF model ###
def get_nmf():
    nmf = NMF(n_components=K, random_state=1, alpha=.1, l1_ratio=.5).fit(X)

    tfidf_feature_names = VECTORIZER.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, 10)
    return nmf


### LDA model ###
def get_lda():
    lda = LatentDirichletAllocation(
        n_topics=K,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0)
    lda.fit(X)
    tf_feature_names = VECTORIZER.get_feature_names()
    print_top_words(lda, tf_feature_names, 10)
    return lda


### DBSCAN ###
def get_dbscan():
    from sklearn.preprocessing import StandardScaler
    X2 = StandardScaler(with_mean=False).fit_transform(X)
    db = DBSCAN(eps=0.3, min_samples=2).fit(X)
    n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print n_clusters_
    return db


############ CREATE RECOMMENDATIONS ############
def load_user_ratings(filename, course_id_lookup, course_doc_dict):
    f = open(filename)
    course_ids = []
    ratings = []
    for line in f:
        class_name, rating = line.split()
        course_id_list = set(course_id_lookup[class_name])
        for course in course_id_list:
            course_ids.append(course)
            ratings.append(float(rating))

    docs = [course_doc_dict[course_id] for course_id in course_ids]
    return course_ids, ratings, docs


def recommend(vectorizer, cluster_func, course_ids, ratings, docs,
              course_doc_dict):
    # import pdb; pdb.set_trace()
    trained_clusterer_docs = cluster_func(vectorizer.transform(docs))
    cluster_scores = np.zeros(K)
    mean_rating = 3
    for trained_clusterer_doc, rating in zip(trained_clusterer_docs, ratings):
        probs = trained_clusterer_doc / sum(trained_clusterer_doc)
        cluster_scores[:] += (rating - mean_rating) * probs

    # import pdb; pdb.set_trace()

    trained_clusterer_all_classes = cluster_func(
        vectorizer.transform(course_doc_dict.values()))
    class_ratings = []
    for trained_clusterer_class in trained_clusterer_all_classes:
        probs = trained_clusterer_class / sum(trained_clusterer_class)
        class_ratings.append(np.dot(probs, cluster_scores))

    class_rankings = sorted(
        list(zip(class_ratings, course_doc_dict.keys())), reverse=True)
    recommendations = []
    for rating, course_id in class_rankings:
        if course_id not in course_ids:
            recommendations.append((course_id, rating))
    # import pdb; pdb.set_trace()
    return recommendations


from sklearn.utils.extmath import row_norms, squared_norm
from sklearn.cluster.k_means_ import _labels_inertia


def km_inertia(km):
    def func(dat_matrix):
        x_squared_norms = row_norms(dat_matrix, squared=True)
        inertias = _labels_inertia(dat_matrix, x_squared_norms,
                                   km.cluster_centers_)[1]
        return inertias

    return func


KM = get_kmeans(X, VECTORIZER)

COURSE_IDS, RATINGS, DOCS = load_user_ratings(
    sys.argv[1], COURSE_ID_LOOKUP_DICT, COURSE_DOC_DICT)
# lda = get_lda()
# RECOMMENDATIONS = recommend(VECTORIZER, lda.transform, COURSE_IDS, RATINGS, DOCS, COURSE_DOC_DICT)
RECOMMENDATIONS = recommend(
    VECTORIZER, lambda x: 1. / (KM.transform(x)**3 + 0.05), COURSE_IDS,
    RATINGS, DOCS, COURSE_DOC_DICT)

print 'Top 40 recommendations:'
for course_id, rating in RECOMMENDATIONS[:40]:
    print CLASS_NUMBER_LOOKUP_DICT[course_id], rating
print 'Bottom 20 recommendations:'
for course_id, rating in RECOMMENDATIONS[-20:]:
    print CLASS_NUMBER_LOOKUP_DICT[course_id], rating
