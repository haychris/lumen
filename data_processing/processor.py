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


# (course_id_lookup_dict, class_number_lookup_dict,
#       course_cluster_probs_dict, k, vectorizer, tfidf_mat, word_dict,
#       course_doc_dict, course_id_list, course_info_dict,
#       course_association_dictionary, pagerank_dict),
#      open(website_necessities_filename, 'wb'))
class FullClassProcessor(object):
    def __init__(self, processed_data_path):
        # auxiliary
        # self.__processed_data = {}

        # continually updated necessities
        self.course_id_lookup_dict = defaultdict(set)
        self.class_number_lookup_dict = defaultdict(set)
        self.course_doc_dict = defaultdict(str)
        self.course_info_dict = None  # TODO: add this

        # necessities that must be rebuilt
        self.vectorizer = None
        self.tfidf_mat = None
        self.word_dict = None

        self.k = None
        self.course_cluster_probs_dict = None

        self.course_association_dictionary = None
        self.course_graph = None
        self.pagerank_dict = None

        term_data_files = os.listdir(processed_data_path)
        for i, file_name in enumerate(term_data_files):
            path = '%s/%s' % (processed_data_path, file_name)
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
              self.course_id_list, self.course_info_dict,
              self.course_association_dictionary, self.pagerank_dict),
             open(file_name, 'wb'))

    def add_course(self, course, rebuild=True):
        self.__update_course_id_lookup(course)
        self.__update_course_doc_dict(course)

        if rebuild:
            self.build()

    def build(self):
        self.__build_word_vec()
        self.__build_clustering()
        self.__build_course_graph()

    def __build_word_vec(self):
        doc_list = self.__get_doc_list()
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
        self.k = 50
        km = KMeans(
            n_clusters=self.k, init='k-means++', max_iter=300, n_init=20)
        km.fit(self.tfidf_mat)

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
        # calculate directed edge weights via number of mentions
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

        # build graph
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

        # perform graph analysis
        self.pagerank_dict = nx.pagerank(self.course_graph)

    def __update_course_id_lookup(self, course):
        for listing in course['listings']:
            name = listing['dept'] + listing['number']
            self.course_id_lookup_dict[name].add(course['courseid'])
            self.class_number_lookup_dict[course['courseid']].add(name)

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
        doc_list.extend(course['reviews'])
        return ' '.join(doc_list)

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
    processed_data_path = '%s/%s' % (root_path, '/course_processed_data/')
    save_path = '%s/%s' % (root_path, '/pickled_data/')
    processor = FullClassProcessor(processed_data_path=processed_data_path)
    processor.save_necessities(save_path)
