import cPickle as pickle

class Course(object):
	ratings_order = {'Lectures':0, 
	'Papers; Reports; Problem Sets; Examinations':1, 
	'Readings':2, 'Classes':3, 'Overall Quality of the Course':4, 
	'Feedback for other students:':5}

	term_ids = {'1142': "Fall '13", '1144': "Spring '14",
	            '1152': "Fall '14", '1154': "Spring '15", 
	            '1162': "Fall '15", '1164': "Spring '16", 
	            '1172': "Fall '16"}
	def __init__(self, term_info_dict):
		self.term_info_dict = term_info_dict
		for term_id in sorted(term_info_dict.keys(), reverse=True):
			if len(self.term_info_dict[term_id]['EVAL']) > 0:
				self.default_term = term_id
				break
		else:
			self.default_term = sorted(term_info_dict.keys())[-1]

	def get_default_term_text(self):
		return self.term_ids[self.default_term]

	def get_title(self, term_id=None):
		if term_id is None:
			return self.term_info_dict[self.default_term]['title']
		else:
			return self.term_info_dict[term_id]['title']
	
	def get_course_listings(self, term_id=None):
		if term_id is None:
			return self.term_info_dict[self.default_term]['all_listings_string']
		else:
			return self.term_info_dict[term_id]['all_listings_string']

	
	def get_comments(self, term_id=None):
		if term_id is None:
			return self.term_info_dict[self.default_term]['COMMENTS']
		else:
			return self.term_info_dict[term_id]['COMMENTS']
	
	def get_all_ratings(self, term_id=None):
		if term_id is None:
			ratings = [rating for name, rating in self.term_info_dict[self.default_term]['EVAL']]
		else:
			ratings = [rating for name, rating in self.term_info_dict[self.default_term]['EVAL']]
		if len(ratings) > 0:
			return ratings
		else:
			return [0]*len(self.ratings_order.keys())
	def get_most_recent_overall_rating(self):
		ratings_list = self.term_info_dict[self.default_term]['EVAL']
		if len(ratings_list) > 0:
			return ratings_list[self.ratings_order['Overall Quality of the Course']][1]
		else:
			return 0

class CourseRenderer(object):
	def __init__(self, filename):
		self.course_info_dict = pickle.load(open(filename, 'rb'))

	def get_course(self, course_id):
		return Course(self.course_info_dict[course_id])