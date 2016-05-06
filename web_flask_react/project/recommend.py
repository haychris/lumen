import cPickle as pickle
import numpy as np

class Recommender(object):
	def __init__(self, filename, mean_rating=3):
		self.mean_rating = mean_rating
		self.course_id_lookup_dict, self.class_number_lookup_dict, self.course_cluster_probs_dict, self.K = pickle.load(open(filename, 'rb'))

	def recommend(self, course_nums, ratings):
		course_ids = [self.course_id_lookup_dict[course_num] for course_num in course_nums]
		cluster_scores = np.zeros(self.K)

		for course_id_list, rating in zip(course_ids, ratings):
			probs = self.course_cluster_probs_dict[course_id_list[0]]
			for course_id in course_id_list[1:]:
				probs += self.course_cluster_probs_dict[course_id_list[0]]
			probs /= len(course_id_list)
			cluster_scores[:] += (rating-self.mean_rating)*probs

		class_ratings = []
		for probs in self.course_cluster_probs_dict.values():
			class_ratings.append(np.dot(probs, cluster_scores))

		class_rankings = sorted(list(zip(class_ratings, self.course_cluster_probs_dict.keys())), reverse=True)
		recommendations = []
		for rating, course_id in class_rankings:
			if course_id not in course_ids:
				recommendations.append((course_id, rating))
		return recommendations

	def course_id_to_course_num(self, course_id):
		return self.class_number_lookup_dict[course_id]

	def course_num_to_course_id(self, course_num):
		return self.course_id_lookup_dict[course_num]