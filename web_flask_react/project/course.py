import cPickle as pickle

class Course(object):
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
	
	def get_ratings(self, term_id=None):
		if term_id is None:
			return self.term_info_dict[self.default_term]['EVAL']
		else:
			return self.term_info_dict[term_id]['EVAL']

class CourseRenderer(object):
	def __init__(self, filename):
		self.course_info_dict = pickle.load(open(filename, 'rb'))

	def get_course(self, course_id):
		return Course(self.course_info_dict[course_id])