import cPickle as pickle
import numpy as np

class Searcher(object):
	def __init__(self, filename):
		self.tfidf_mat, self.word_dict, self.course_doc_dict = pickle.load(open(filename, 'rb'))
		self.doc_course_id_list = self.course_doc_dict.keys()

	def search(self, term_list, num_results=20):
			# results = self.tfidf_mat[:,self.word_dict[term_list[0]]]
		# import pdb; pdb.set_trace()
		results = np.zeros((self.tfidf_mat.shape[0],1))
		for term in term_list:
			try:
				results += self.tfidf_mat[:,self.word_dict[term]]
			except KeyError:
				continue
		sorted_docs = np.argsort(results[np.nonzero(results)])
		# import pdb; pdb.set_trace()
		try:
			return [self.doc_course_id_list[sorted_docs[0,-(i+1)]] for i in range(min(num_results, sorted_docs.shape[1]))]
		except IndexError:
			return []