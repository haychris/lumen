import cPickle as pickle

class Course(object):
	ratings_order = {'Lectures':0, 
	'Papers; Reports; Problem Sets; Examinations':1, 
	'Readings':2, 'Classes':3, 'Overall Quality of the Course':4, 
	'Feedback for other students:':5}
	def __init__(self, term_info_dict):
		self.term_info_dict = term_info_dict
		self.default_term = sorted(term_info_dict.keys())[-1]

	def get_title(self, term_id=None):
		if term_id is None:
			return self.term_info_dict[self.default_term]['COURSE_TITLE']
		else:
			return self.term_info_dict[term_id]['COURSE_TITLE']
	
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