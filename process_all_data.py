import sys
from collections import defaultdict
import pandas as pd

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
	add_registrar('spring_15_features.csv', class_dict)
	add_registrar('fall_15_features.csv', class_dict)
	create_documents(class_dict)

	return class_dict

def get_doc_list(class_dict):
	doc_dict = defaultdict(list)
	for term_dict in class_dict.values():
		for course_id, course_dict in term_dict.items():
			doc_dict[course_id].append(course_dict['document'])
	doc_list = [' '.join(docs) for docs in doc_dict.values()]
	return doc_list

def get_tfidf_matrix(doc_list):
	from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
	vectorizer = TfidfVectorizer(input='content', max_df=0.5, stop_words='english', use_idf=True, min_df=2)
	vectorizer.fit(doc_list)
	X = vectorizer.transform(doc_list)
	return vectorizer, X
