import sys
from collections import defaultdict
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans

def add_ratings(file_name, class_dict):
	f = open(file_name)
	header = f.readline().replace("\n", "")
	column_keys = header.split(',')
	# column_keys = ["STRM","SUBJECT","CATALOG_NBR","PU_EVAL_CATEGORY","CRSE_ID","PU_EVAL_MEAN"]
	for line in f:
		line_dict = {column_keys[i]:val for i, val in enumerate(line.split(','))}
		cur_term_dict = class_dict[line_dict["STRM"]]
		cur_course_dict = cur_term_dict[line_dict["CRSE_ID"]]
		cur_course_dict["SUBJECT"] = line_dict["SUBJECT"]
		cur_course_dict["CATALOG_NBR"] = line_dict["CATALOG_NBR"]
		cur_course_dict["EVAL"].append((line_dict["PU_EVAL_CATEGORY"], float(line_dict["PU_EVAL_MEAN"])))


# for file_name in sys.argv[2:]:
def add_comments(file_name, class_dict):
	f = open(file_name)
	cur_header = f.readline().replace('\n', '')
	cur_column_keys = filter(None, cur_header.split(','))
	# cur_column_keys = ["STRM", "SUBJECT", "CATALOG_NBR", "CRSE_ID", "COURSE_TITLE", "PU_EVAL_COMMENTS"]
	split = None
	for line in f:
		split = filter(None, line.replace('\n', '').split(','))
		if len(split) == 0:
			continue
		try:
			strm = split[0]
			test_strm = int(strm)
			subject = split[1]
			catalog_nbr = split[2]
			test_catalog_nbr = int(catalog_nbr)
			crse_id = split[3]
			course_title = split[4]
			comments = ' '.join(split[5:])
			prev_split = split
		except (IndexError, ValueError) as e:
			print 'IndexError. SKIPPING'
			continue
			# strm = prev_split[0]
			# subject = prev_split[1]
			# catalog_nbr = prev_split[2]
			# crse_id = prev_split[3]
			# course_title = prev_split[4]
			# comments = ' '.join(split)
			
		# line_dict = {cur_column_keys[i]:val for i, val in enumerate(filter(None, ))}
		cur_term_dict = class_dict[strm]
		cur_course_dict = cur_term_dict[crse_id]
		cur_course_dict["SUBJECT"] = subject
		cur_course_dict["CATALOG_NBR"] = catalog_nbr
		cur_course_dict["COURSE_TITLE"] = course_title
		cur_course_dict["COMMENTS"].append(comments)
		# try:
		# 	cur_course_dict["COMMENTS"].append(line_dict["PU_EVAL_COMMENTS"])
		# except KeyError:
		# 	cur_course_dict["COMMENTS"].append(line_dict["COMMENTS"])
def add_registrar(file_name, class_dict):
	f = open(file_name)
	header = f.readline()
	column_keys = header.replace('\n', '').split(',')
	# column_keys = termid,courseid,title,all_listings_string,area,prereqs,descrip

			
	# class_dict = defaultdict(lambda : defaultdict(lambda: defaultdict(list)))
	for line in f:
		line = line.replace('\n', '').replace('"', '')
		line_dict = {column_keys[i]:val for i, val in enumerate(line.split(','))}
		cur_term_dict = class_dict[line_dict["termid"]]
		cur_course_dict = cur_term_dict[str(int(line_dict["courseid"]))]
		cur_course_dict["all_listings_string"] = line_dict["all_listings_string"]
		cur_course_dict["area"] = line_dict["area"]
		cur_course_dict["title"] = line_dict["title"]
		cur_course_dict["prereqs"] = line_dict["prereqs"]
		cur_course_dict["descrip"] = line_dict["descrip"]
		cur_course_dict['prof_string'] = line_dict['prof_string']


def create_documents(class_dict):
	for term_dict in class_dict.values():
		for course_dict in term_dict.values():
			doc_list = []
			for value in course_dict.values():
				if isinstance(value, list):
					for item in value:
						if isinstance(item, str):
							doc_list.append(item)
				else:
					doc_list.append(value)
			course_dict['document'] = ' '.join(doc_list)

def get_class_dict():
	class_dict = defaultdict(lambda : defaultdict(lambda: defaultdict(list)))
	add_ratings('aggregates.csv', class_dict)
	add_comments('comments_pt_1.csv', class_dict)
	add_comments('comments_pt_2.csv', class_dict)
	add_registrar('spring_16_features.csv', class_dict)
	add_registrar('fall_15_features.csv', class_dict)
	add_registrar('spring_15_features.csv', class_dict)
	add_registrar('fall_14_features.csv', class_dict)
	add_registrar('spring_14_features.csv', class_dict)
	add_registrar('fall_13_features.csv', class_dict)

	create_documents(class_dict)

	return class_dict

def get_course_id_lookup_dict(class_dict):
	course_id_lookup_dict = defaultdict(list)
	class_number_lookup_dict = defaultdict(list)
	for term_dict in class_dict.values():
		for course_id, course_dict in term_dict.items():
			class_listing = course_dict["all_listings_string"]
			if isinstance(class_listing, list):
				class_listing = ' '.join(class_listing)
			classes = class_listing.split()
			for i in range(0,len(classes), 2):
				course_id_lookup_dict[classes[i] + classes[i+1]].append(course_id)
				class_number_lookup_dict[course_id].append(classes[i] + classes[i+1])
			if len(classes) == 0:
				course_id_lookup_dict[course_dict["SUBJECT"] + course_dict["CATALOG_NBR"]].append(course_id)
				class_number_lookup_dict[course_id].append(course_dict["SUBJECT"] + course_dict["CATALOG_NBR"])
	for key, value in course_id_lookup_dict.items():
		course_id_lookup_dict[key] = list(set(value))
	for key, value in class_number_lookup_dict.items():
		class_number_lookup_dict[key] = list(set(value))
	return course_id_lookup_dict, class_number_lookup_dict
			

def get_doc_list(class_dict):
	doc_dict = defaultdict(list)
	for term_dict in class_dict.values():
		for course_id, course_dict in term_dict.items():
			doc_dict[course_id].append(course_dict['document'])
	course_doc_dict = {course_id:' '.join(docs) for course_id, docs in doc_dict.items()}
	course_id_list = course_doc_dict.keys()
	doc_list = course_doc_dict.values()
	return course_doc_dict, course_id_list, doc_list

from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 

class LemmaTokenizer(object):
	def __init__(self):
		self.wnl = WordNetLemmatizer()
	def __call__(self, doc):
		tokens =  [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
		return [w.lower() for w in tokens if w.isalpha()]

def get_tfidf_matrix(doc_list):
	from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
	vectorizer = TfidfVectorizer(input='content', max_df=0.9, stop_words='english', use_idf=True, min_df=2, tokenizer=LemmaTokenizer())
	vectorizer.fit(doc_list)
	X = vectorizer.transform(doc_list)
	return vectorizer, X

def get_all(filename, generate=False):
	# import cPickle as pickle
	if generate:
		from cloud.serialization.cloudpickle import dump
		class_dict = get_class_dict()
		course_id_lookup_dict, class_number_lookup_dict = get_course_id_lookup_dict(class_dict)
		course_doc_dict, course_id_list, doc_list = get_doc_list(class_dict)
		vectorizer, tfidf_mat = get_tfidf_matrix(doc_list)
		dump((class_dict, course_id_lookup_dict, class_number_lookup_dict, course_doc_dict, doc_list, vectorizer, tfidf_mat), open(filename, 'wb'))
	else:
		import cPickle as pickle
		class_dict, course_id_lookup_dict, class_number_lookup_dict, course_doc_dict, doc_list, vectorizer, tfidf_mat = pickle.load(open(filename, 'rb'))
	return class_dict, course_id_lookup_dict, class_number_lookup_dict, course_doc_dict, doc_list, vectorizer, tfidf_mat


recommender_necessities_filename = 'recommender_necessities.pickle'
search_necessities_filename = 'search_necessities.pickle'
course_info_necessities_filename = 'course_info_necessities.pickle'
def process_website_necessities():
	class_dict = get_class_dict()
	course_doc_dict, course_id_list, doc_list = get_doc_list(class_dict)
	vectorizer, tfidf_mat = get_tfidf_matrix(doc_list)

	k = 50
	km = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=20)
	km.fit(tfidf_mat)

	similarity_func = lambda x: 1./(km.transform(x)**3+0.05)

	similarities_all_classes = similarity_func(vectorizer.transform(course_doc_dict.values()))
	course_cluster_probs_dict = {}
	for course_id, cur_class_similarities in zip(course_doc_dict.keys(), similarities_all_classes):
		probs = cur_class_similarities / sum(cur_class_similarities)
		course_cluster_probs_dict[course_id] = probs


	course_id_lookup_dict, class_number_lookup_dict = get_course_id_lookup_dict(class_dict)

	from cloud.serialization.cloudpickle import dump
	dump((course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k), open(recommender_necessities_filename, 'wb'))

	feat_names = vectorizer.get_feature_names()
	word_dict = {}
	for i, name in enumerate(feat_names):
		word_dict[name] = i

	dump((vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list), open(search_necessities_filename, 'wb'))

	course_info_dict = {}
	for course_id in class_number_lookup_dict.keys():
		term_info_dict = {}
		for term_id, term_dict in class_dict.items():
			if course_id in term_dict:
				term_info_dict[term_id] = class_dict[term_id][course_id]
		course_info_dict[course_id] = term_info_dict
	dump(course_info_dict, open(course_info_necessities_filename, 'wb'))





