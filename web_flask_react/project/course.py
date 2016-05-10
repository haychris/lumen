import cPickle as pickle
import re
import itertools

def safe_convert(x):
	try:
		return unicode(x, 'utf-8', errors='ignore')
	except (TypeError, UnicodeDecodeError) as e:
		return x


def minimizer(x,y):
	if (0 < len(x) < len(y)) or len(y) == 0:
		return safe_convert(x)
	return safe_convert(y)

class Course(object):
	ratings_order = {'Lectures':0, 
	'Papers; Reports; Problem Sets; Examinations':1, 
	'Readings':2, 'Classes':3, 'Overall Quality of the Course':4, 
	'Feedback for other students:':5}

	term_ids = {'1142': "Fall '13", '1144': "Spring '14",
	            '1152': "Fall '14", '1154': "Spring '15", 
	            '1162': "Fall '15", '1164': "Spring '16", 
	            '1172': "Fall '16"}
	def __init__(self, term_info_dict, planner, course_id):
		self.course_id = course_id
		self.term_info_dict = term_info_dict
		self.planner = planner
		for term_id in sorted(term_info_dict.keys(), reverse=True):
			if len(self.term_info_dict[term_id]['EVAL']) > 0:
				self.default_term = term_id
				break
		else:
			self.default_term = sorted(term_info_dict.keys())[-1]

	def get_url_courseid(self):
		return '0'*(6-len(self.course_id)) + self.course_id

	def get_default_term_text(self):
		return self.term_ids[self.default_term]

	def get_title(self, term_id=None):
		if term_id is None:
			term_id = self.default_term
		title = self.term_info_dict[term_id]['title']
		if not title:
			title = self.term_info_dict[term_id]['COURSE_TITLE']
		return title

	def get_course_listings(self, term_id=None):
		if term_id is None:
			term_id = self.default_term
		listings = self.term_info_dict[term_id]['all_listings_string']
		if not listings:
			listings = self.term_info_dict[term_id]['SUBJECT'] + ' ' + self.term_info_dict[term_id]['CATALOG_NBR']
		return listings

	def processed_course_listings(self, term_id=None):
		course_listings = self.get_course_listings(term_id)
		split_course_listings = course_listings.split()
		new_course_listings = ' '.join(split_course_listings[:4])
		if len(split_course_listings) > 4:
			new_course_listings += '...'
		return new_course_listings

	def get_list_of_course_nums(self, term_id=None):
		listings = self.get_course_listings(term_id).split()
		course_num_list = []
		for i in range(0, len(listings), 2):
			course_num_list.append(listings[i]+listings[i+1])
		return course_num_list

	def get_professors(self, term_id=None):
		if term_id is None:
			term_id = self.default_term
		profs = self.term_info_dict[term_id]['prof_string']
		if not profs:
			profs = ''
		return unicode(profs, 'utf-8')

	# !!!!!!!!!!! 
	def get_first_professor(self, profs):
		return profs.split('|')[0]

	def get_comments(self, term_id=None):
		if term_id is None:
			term_id = self.default_term
		return self.term_info_dict[term_id]['COMMENTS']
	
	def get_all_ratings(self, term_id=None):
		if term_id is None:
			term_id = self.default_term
		ratings = [rating for name, rating in self.term_info_dict[term_id]['EVAL']]

		if len(ratings) > 0:
			return ratings
		else:
			return [0]*len(self.ratings_order.keys())

	def get_most_recent_overall_rating(self):
		ratings_list = self.term_info_dict[self.default_term]['EVAL']
		if len(ratings_list) > 0:
			try:
				return ratings_list[self.ratings_order['Overall Quality of the Course']][1]
			except IndexError:
				# import pdb; pdb.set_trace()
				return 0
		else:
			return 0

	def get_highlighted_text(self, terms):
		if len(terms) == 0:
			return ''
		top_num = -1
		top_comment = ''
		second_num = -1
		second_comment = ''
		for term_id, info_dict in self.term_info_dict.items():
			for comment in info_dict["COMMENTS"]:
				num_terms = 0
				for term in terms:
					if term in safe_convert(comment):
						num_terms += 1
				if num_terms > top_num:
					second_num = top_num
					second_comment = top_comment
					top_num = num_terms
					top_comment = comment
				elif num_terms > second_num:
					second_num = num_terms
					second_comment = comment
		if top_comment == second_comment:
			second_comment = ''

		for term in terms:
			top_comment = top_comment.replace(term, '<u><b>' + term + '</b></u>')
			second_comment = second_comment.replace(term, '<u><b>' + term + '</b></u>')
		return safe_convert(top_comment), safe_convert(second_comment)
		# doc =  self.term_info_dict[self.default_term]['document'].lower()
		# results = []
		# for term_list in itertools.permutations(terms):
		# 	pattern = ' .*? '.join(terms)
		# 	pattern = '.{0,20}' + pattern + '.{0,20}'
		# 	results.extend(re.findall(pattern, doc))
		# # import pdb; pdb.set_trace()
		# if len(results) > 0:
		# 	return '...' + reduce(minimizer, results) + '...'
		# else:
		# 	# import pdb; pdb.set_trace()
		# 	new_term_lists = [list(terms) for _ in range(len(terms))]
		# 	for i,term in enumerate(terms):
		# 		new_term_lists[i].remove(term)
		# 	new_results = [self.get_highlighted_text(new_term_lists[i]) for i in range(len(terms))]
		# 	# import pdb; pdb.set_trace()
		# 	return reduce(minimizer, new_results)

class CourseRenderer(object):
	def __init__(self, course_info_dict, planner):
		# self.course_info_dict = pickle.load(open(filename, 'rb'))
		self.course_info_dict = course_info_dict
		self.planner = planner
		
	def get_course(self, course_id):
		return Course(self.course_info_dict[course_id], self.planner, course_id)
