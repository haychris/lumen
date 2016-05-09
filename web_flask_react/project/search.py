import cPickle as pickle
import numpy as np

class Searcher(object):
	def __init__(self, filename):
		self.vectorizer, self.tfidf_mat, self.word_dict, self.course_doc_dict, self.course_id_list = pickle.load(open(filename, 'rb'))
		self.tokenizer = self.vectorizer.get_params()['tokenizer']

	def add_planner(self, planner):
		self.planner = planner

	def search(self, term_string, major, certificate, num_results=20):
		# term_list = self.vectorizer.transform(term_list)
		term_list = self.tokenizer(term_string)
		major_boost_vector = self.planner.get_major_boost_vector(major, 1.3)
		certificate_boost_vector = self.planner.get_certificate_boost_vector(certificate, 1.2)
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
		results *= major_boost_vector * certificate_boost_vector
		# import pdb; pdb.set_trace()
		sorted_docs = np.argsort(results)[::-1]
		vals = np.sort(results)[::-1]
		first_zero = np.argmin(vals)
		last_index = first_zero 
		if float(vals[first_zero]) == 0:
			last_index -= 1
		if last_index > 0:
			courses = [self.course_id_list[doc_num] for doc_num in sorted_docs[:min(last_index, num_results)]]
		else:
			courses = []
		# import pdb; pdb.set_trace()
		return courses
		# try:
		# 	return [self.doc_course_id_list[sorted_docs[0,-(i+1)]] for i in range(min(num_results, sorted_docs.shape[1]))]
		# except IndexError:
		# 	return []
	