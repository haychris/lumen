import os
import sys
import json
import re
from collections import defaultdict

from cloud.serialization.cloudpickle import dump

from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.cluster import KMeans

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

import networkx as nx

from gensim.models import Word2Vec


class LemmaTokenizer(object):
    distributions = ['LA', 'HA', 'SA', 'EM', 'STN', 'STL', 'QR', 'EC', 'W']

    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        tokens = [self.filtered_lemmatization(t) for t in word_tokenize(doc)]
        return [w.lower() for w in tokens]

    def filtered_lemmatization(self, x):
        if len(x) == 3:
            # floor 3 digit nums by hundred, i.e., '323' -> '300'
            if x.isdigit():
                return str(int(x) / 100 * 100)
            else:
                return x
        if len(x) == 2 and x.upper() in self.distributions:
            return x
        return self.wnl.lemmatize(x)


class FullClassProcessor(object):
    def __init__(self, processed_data_path, verbose=False):
        # auxiliary
        # self.__processed_data = {}
        self.verbose = verbose

        # continually updated necessities
        self.course_id_lookup_dict = defaultdict(set)
        self.class_number_lookup_dict = defaultdict(set)
        self.course_doc_dict = defaultdict(str)
        self.course_info_dict = defaultdict(dict)

        # necessities that must be rebuilt
        self.vectorizer = None
        self.tfidf_mat = None
        self.word_dict = None
        self.word2vec = None

        self.k = None
        self.course_cluster_probs_dict = None

        self.course_association_dictionary = None
        self.course_graph = None
        self.pagerank_dict = None

        term_data_files = os.listdir(processed_data_path)
        for i, file_name in enumerate(term_data_files):
            path = '%s/%s' % (processed_data_path, file_name)
            if self.verbose:
                print 'Adding ', path
            f = open(path)
            term_data = json.load(f)
            f.close()

            # self.__processed_data[term] = term_data

            for course in term_data:
                self.add_course(course, False)
        self.build()

    def save_necessities(self, file_name):
        dump((self.course_id_lookup_dict, self.class_number_lookup_dict,
              self.course_cluster_probs_dict, self.k, self.vectorizer,
              self.tfidf_mat, self.word_dict, self.course_doc_dict,
              self.__get_course_id_list(), self.course_info_dict,
              self.course_association_dictionary, self.pagerank_dict),
             open(file_name, 'wb'))

    def add_course(self, course, rebuild=True):
        self.__update_course_id_lookup(course)
        self.__update_course_info_dict(course)
        self.__update_course_doc_dict(course)

        if rebuild:
            self.build()

    def build(self):
        self.__build_word_vec()
        self.__build_clustering()
        self.__build_course_graph()

    def __get_sentences(self):
        doc_list = self.__get_doc_list()
        tokenizer = LemmaTokenizer()
        all_doc_sentences = []
        for doc in doc_list:
            all_doc_sentences.append(tokenizer(doc))
        return all_doc_sentences

    def __build_word_vec(self):
        if self.verbose:
            print 'Building word vectorizer and tfidf_mat'
        doc_list = self.__get_doc_list()

        all_doc_sentences = self.__get_sentences()
        self.word2vec = Word2Vec(
            all_doc_sentences, size=100, min_count=2, workers=4)
        # import matplotlib.pyplot as plt
        # from sklearn.decomposition import PCA
        # keys = self.word2vec.vocab.keys()
        # weights = [self.word2vec[key] for key in keys]
        # pca = PCA(n_components=2)
        # pca.fit(weights)
        # dat = pca.transform(weights)
        # xs = [x[0] for x in dat]
        # ys = [x[1] for x in dat]
        # fig, ax = plt.subplots()
        # ax.scatter(xs, ys)
        #
        # for i, txt in enumerate(keys):
        #     ax.annotate(txt, (xs[i], ys[i]))
        # plt.show()
        # import pdb; pdb.set_trace()
        self.vectorizer = TfidfVectorizer(
            input='content',
            max_df=0.9,
            stop_words='english',
            use_idf=True,
            min_df=2,
            tokenizer=LemmaTokenizer())
        self.vectorizer.fit(doc_list)
        self.tfidf_mat = self.vectorizer.transform(doc_list)

        feat_names = self.vectorizer.get_feature_names()
        self.word_dict = {}
        for i, name in enumerate(feat_names):
            self.word_dict[name] = i

    def __get_doc_list(self):
        return self.course_doc_dict.values()

    def __get_course_id_list(self):
        return self.course_doc_dict.keys()

    def __build_clustering(self):
        if self.verbose:
            print 'Running KMeans clustering'
        self.k = 50
        km = KMeans(
            n_clusters=self.k, init='k-means++', max_iter=300, n_init=20)
        km.fit(self.tfidf_mat)

        if self.verbose:
            print 'Calculating similarity to cluster means for each class'

        def similarity_func(x):
            return 1. / (km.transform(x)**3 + 0.05)

        similarities_all_classes = similarity_func(
            self.vectorizer.transform(self.course_doc_dict.values()))
        self.course_cluster_probs_dict = {}
        for course_id, cur_class_similarities in zip(
                self.course_doc_dict.keys(), similarities_all_classes):
            probs = 1.0 * cur_class_similarities / sum(cur_class_similarities)
            self.course_cluster_probs_dict[course_id] = probs

    def __build_course_graph(self):
        if self.verbose:
            print "calculating directed edge weights via number of mentions"
        self.course_association_dictionary = defaultdict(
            lambda: defaultdict(int))
        for course_id, doc in self.course_doc_dict.items():
            for other_course_num in self.course_id_lookup_dict.keys():
                pattern = other_course_num[:3] + ' ' + other_course_num[3:]
                if re.search(pattern, doc):
                    for other_course_id in self.course_id_lookup_dict[
                            other_course_num]:
                        self.course_association_dictionary[course_id][
                            other_course_id] += 1

        if self.verbose:
            print "building course graph"
        self.course_graph = nx.Graph()
        self.course_graph.add_nodes_from(self.__get_course_id_list())
        for course_id, mentions_dict in self.course_association_dictionary.items(
        ):
            for mention, num in mentions_dict.items():
                if not course_id == mention:
                    if (course_id, mention) in self.course_graph.edges():
                        self.course_graph.add_edge(
                            course_id,
                            mention,
                            weight=num + self.course_graph.edge[course_id][
                                mention]['weight'])
                    elif (mention, course_id) in self.course_graph.edges():
                        self.course_graph.add_edge(
                            mention,
                            course_id,
                            weight=num + self.course_graph.edge[mention][
                                course_id]['weight'])
                    else:
                        self.course_graph.add_edge(
                            course_id, mention, weight=num)

        if self.verbose:
            print "performing graph analysis (calculating pagerank)"
        self.pagerank_dict = nx.pagerank(self.course_graph)

    def __update_course_id_lookup(self, course):
        for listing in course['listings']:
            name = listing['dept'] + listing['number']
            self.course_id_lookup_dict[name].add(course['courseid'])
            self.class_number_lookup_dict[course['courseid']].add(name)

    def __update_course_info_dict(self, course):
        course_id = course['courseid']
        term_id = course['termid']
        course['prof_string'] = self.get_prof_string(course)
        course['all_listings_string'] = self.get_listings_string(course)
        course['document'] = self.make_document(course)
        self.course_info_dict[course_id][term_id] = course

    def __update_course_doc_dict(self, course):
        doc = self.make_document(course)
        self.course_doc_dict[course['courseid']] += ' ' + doc

    def make_document(self, course):
        doc_list = []
        doc_list.append(self.get_prof_string(course))
        doc_list.append(course['area'])
        doc_list.append(self.get_listings_string(course))
        doc_list.append(course['prereqs'])
        doc_list.append(course['descrip'])
        doc_list.append(course['title'])
        doc_list.extend(self.get_reviews(course))
        return ' '.join(doc_list)

    def get_reviews(self, course):
        if 'reviews' in course and course['reviews'] is not None:
            return filter(bool, course['reviews'])
        else:
            return []

    def get_prof_string(self, course):
        return ' | '.join([prof['name'] for prof in course['profs']])

    def get_listings_string(self, course):
        listings = [
            listing['dept'] + ' ' + listing['number']
            for listing in course['listings']
        ]
        return ' | '.join(listings)


if __name__ == "__main__":
    root_path = '/'.join(sys.argv[0].split('/')[:-1])
    processed_data_path = '%s/%s' % (root_path, 'course_processed_data')
    save_path = '%s/%s' % (root_path, 'pickled_data/necessities.pickle')
    processor = FullClassProcessor(
        processed_data_path=processed_data_path, verbose=True)
    processor.save_necessities(save_path)
