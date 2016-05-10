import cPickle as pickle
import numpy as np

class Searcher(object):
	def __init__(self, vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_id_lookup_dict, class_number_lookup_dict, planner):
		# self.vectorizer, self.tfidf_mat, self.word_dict, self.course_doc_dict, self.course_id_list = pickle.load(open(filename, 'rb'))
		self.vectorizer = vectorizer
		self.tfidf_mat = tfidf_mat
		self.word_dict = word_dict
		self.course_doc_dict = course_doc_dict
		self.course_id_list = course_id_list
		self.tokenizer = self.vectorizer.get_params()['tokenizer']
		self.course_id_lookup_dict = course_id_lookup_dict
		self.class_number_lookup_dict = class_number_lookup_dict
		self.planner = planner

	# def add_planner(self, planner):
	# 	self.planner = planner

	def search(self, term_string, major, certificate, num_results=20):
		major_boost_vector = self.planner.get_major_boost_vector(major, 1.3)
		certificate_boost_vector = self.planner.get_certificate_boost_vector(certificate, 1.2)
		pagerank_boost_vector = self.planner.get_pagerank_boost_vector(1.1)
		overall_boost = major_boost_vector * certificate_boost_vector * pagerank_boost_vector


		term_list = self.tokenizer(term_string)
		print term_list
			# results = self.tfidf_mat[:,self.word_dict[term_list[0]]]
		# import pdb; pdb.set_trace()
		results = np.zeros((self.tfidf_mat.shape[0],1))
		for term in term_list:
			try:
				results += self.tfidf_mat[:,self.word_dict[term]]
			except KeyError:
				continue
		results = np.array(results).ravel()
		results /= np.max(results)
		results *= overall_boost
		# import pdb; pdb.set_trace()
		sorted_docs = np.argsort(results)[::-1]
		vals = np.sort(results)[::-1]
		first_zero = np.argmin(vals)
		last_index = first_zero 
		if float(vals[first_zero]) == 0:
			last_index -= 1
		if last_index > 0:
			courses = [self.course_id_list[doc_num] for doc_num in sorted_docs[:last_index]]
		else:
			courses = []
		# import pdb; pdb.set_trace()
		split_terms = term_string.split()
		if len(split_terms) == 1 and len(term_string) == 6:
			split_terms = [term_string[:3], term_string[3:]]
		if len(split_terms) == 2 and split_terms[0].isalpha() and len(split_terms[0]) == 3 and split_terms[1].isdigit() and len(split_terms[1]) == 3:
			specific_courses = self.course_id_lookup_dict[term_string.upper().replace(' ', '')]
			for spe_course in reversed(specific_courses):
				try:
					courses.remove(spe_course)
				except ValueError:
					pass
				courses.insert(0, spe_course)

		recommendations = []
		for cur_id in courses:
			if len(recommendations) >= num_results:
				break
			if not any(map(lambda x: 'FRS' in x, self.class_number_lookup_dict[cur_id])):
				recommendations.append(cur_id)
		return recommendations
		# try:
		# 	return [self.doc_course_id_list[sorted_docs[0,-(i+1)]] for i in range(min(num_results, sorted_docs.shape[1]))]
		# except IndexError:
		# 	return []
	