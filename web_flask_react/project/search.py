import cPickle as pickle
import numpy as np

class Searcher(object):
	def __init__(self, filename):
		self.tfidf_mat, self.word_dict, self.course_doc_dict = pickle.load(open(filename, 'rb'))
		self.doc_course_id_list = self.course_doc_dict.keys()

	def search(self, term_list, num_results=20):
		results = self.tfidf_mat[:,self.word_dict[term_list[0]]]
		for term in term_list[1:]:
			results += self.tfidf_mat[:,self.word_dict[term]]
		sorted_docs = np.argsort(results.toarray(), axis=0)[::-1]
		return [self.doc_course_id_list[doc_num] for doc_num in sorted_docs[:num_results]]