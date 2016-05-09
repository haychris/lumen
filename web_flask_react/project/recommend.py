import cPickle as pickle
import numpy as np

class Recommender(object):
	def __init__(self, course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, K, course_id_list, planner, mean_rating=3):
		self.mean_rating = mean_rating
		# self.course_id_lookup_dict, self.class_number_lookup_dict, course_cluster_probs_dict, self.K = pickle.load(open(filename, 'rb'))
		self.course_id_lookup_dict = course_id_lookup_dict
		self.class_number_lookup_dict = class_number_lookup_dict
		self.course_cluster_probs_dict = course_cluster_probs_dict
		self.K = K
		self.course_id_list = course_id_list
		self.planner = planner
		self.cluster_probs = [course_cluster_probs_dict[course_id] for course_id in self.course_id_list]

	def recommend(self, course_nums, ratings, major, certificate, num_results=20):
		##### STILL NEED TO BOOST BY CERTIFICATE/MAJOR #####
		course_ids = []
		for course_num in course_nums:
			course_id_list = self.course_id_lookup_dict[course_num]
			if course_id_list:
				course_ids.append(course_id_list)
			
		cluster_scores = np.zeros(self.K)

		for course_id_list, rating in zip(course_ids, ratings):
			probs = self.course_cluster_probs_dict[course_id_list[0]]
			for course_id in course_id_list[1:]:
				probs += self.course_cluster_probs_dict[course_id_list[0]]
			probs /= len(course_id_list)
			cluster_scores[:] += (rating-self.mean_rating)*probs

		major_boost_vector = self.planner.get_major_boost_vector(major, 1.3)
		certificate_boost_vector = self.planner.get_certificate_boost_vector(certificate, 1.2)

		class_ratings = []
		for probs in self.cluster_probs:
			class_ratings.append(np.dot(probs, cluster_scores))

		base_exp = 15
		class_ratings = (np.array(class_ratings)**base_exp) * major_boost_vector * certificate_boost_vector
		sorted_docs = np.argsort(class_ratings)[::-1]
		recommendations = [self.course_id_list[doc_num] for doc_num in sorted_docs[:num_results]]
		# class_rankings = sorted(list(zip(class_ratings, self.course_id_list)), reverse=True)
		# recommendations = []
		# for rating, course_id in class_rankings:
		# 	if course_id not in course_ids:
		# 		recommendations.append((course_id, rating))
		return recommendations

	def course_id_to_course_num(self, course_id):
		return self.class_number_lookup_dict[course_id]

	def course_num_to_course_id(self, course_num):
		return self.course_id_lookup_dict[course_num]