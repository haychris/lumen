import cPickle as pickle
import numpy as np
import math


class Recommender(object):
    def __init__(self,
                 course_id_lookup_dict,
                 class_number_lookup_dict,
                 course_cluster_probs_dict,
                 K,
                 course_id_list,
                 planner,
                 mean_rating=3):
        self.mean_rating = mean_rating
        # self.course_id_lookup_dict, self.class_number_lookup_dict, course_cluster_probs_dict, self.K = pickle.load(open(filename, 'rb'))
        self.course_id_lookup_dict = course_id_lookup_dict
        self.class_number_lookup_dict = class_number_lookup_dict
        self.course_cluster_probs_dict = course_cluster_probs_dict
        self.K = K
        self.course_id_list = course_id_list
        self.planner = planner
        self.cluster_probs = [
            course_cluster_probs_dict[course_id]
            for course_id in self.course_id_list
        ]

    def recommend(self,
                  course_nums,
                  ratings,
                  major,
                  certificate,
                  num_results=20):
        ##### STILL NEED TO BOOST BY CERTIFICATE/MAJOR #####
        course_ids = []
        course_id_taken = []
        for course_num in course_nums:
            cur_course_id_list = self.course_id_lookup_dict[course_num]
            if cur_course_id_list:
                course_ids.append(cur_course_id_list)
                course_id_taken.extend(cur_course_id_list)

        cluster_scores = np.zeros(self.K)

        for cur_course_id_list, rating in zip(course_ids, ratings):
            probs = self.course_cluster_probs_dict[cur_course_id_list[0]]
            for course_id in cur_course_id_list[1:]:
                probs += self.course_cluster_probs_dict[course_id]
            probs /= len(cur_course_id_list)
            cluster_scores[:] += (rating - self.mean_rating) * probs

        major_boost_vector = self.planner.get_major_boost_vector(major, 1.007)
        certificate_boost_vector = self.planner.get_certificate_boost_vector(
            certificate, 1.005)
        pagerank_boost_vector = self.planner.get_pagerank_boost_vector(1.05)

        overall_boost = major_boost_vector * certificate_boost_vector * pagerank_boost_vector
        ### DEBUG
        for i, boost in enumerate(overall_boost):
            if boost > 1:
                print boost, self.class_number_lookup_dict[self.course_id_list[
                    i]]
        ###

        class_ratings = []
        for probs in self.cluster_probs:
            class_ratings.append(np.dot(probs, cluster_scores))

        base_exp = 15
        # import pdb; pdb.set_trace()

        class_ratings = np.log((np.array(class_ratings) + 1)**base_exp)
        class_ratings /= np.max(class_ratings)
        class_ratings *= overall_boost
        sorted_docs = np.argsort(class_ratings)[::-1]
        sorted_ratings = np.sort(class_ratings)[::-1]  ###### FOR DEBUGGING
        print sorted_ratings[:20]
        recommendations = []
        for doc_num in sorted_docs:
            if len(recommendations) >= num_results:
                break
            cur_id = self.course_id_list[doc_num]
            if cur_id not in course_id_taken and not any(
                    map(lambda x: 'FRS' in x or 'WRI' in x,
                        self.class_number_lookup_dict[cur_id])):
                recommendations.append(cur_id)
        # recommendations = [self.course_id_list[doc_num] for doc_num in sorted_docs[:num_results]]
        # import pdb; pdb.set_trace()
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
