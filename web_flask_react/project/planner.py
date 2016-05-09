
class Planner(object):
	major_type_col = 0
	major_col = 1
	def __init__(self, majors_filename, certificates_filename):
		##### HANDLE MAJORS #####
		self.major_requirements = {}
		f = open(majors_filename)
		split = None
		for line in f:
			split = filter(None, line.replace('\n', '').split(','))
			if len(split) == 0:
				continue
			cur_major_info_dict = {}
			cur_major_info_dict['major_type'] = split[self.major_type_col]
			cur_major_info_dict['requirements'] = list(split[max(self.major_col, self.major_type_col):])

			requirement_list = []
			for requirement in cur_major_info_dict['requirements']:
				courses = requirement.split('|')
				requirement_list.extend(courses)
			cur_major_info_dict['requirement_set'] = set(requirement_list)

			major = split[self.major_col]
			self.major_requirements[major] = cur_major_info_dict

		##### HANDLE CERTIFICATES #####
		self.certificate_requirements = {}
		f = open(certificates_filename)
		split = None
		for line in f:
			split = filter(None, line.replace('\n', '').split(','))
			if len(split) == 0:
				continue

			cur_certificate_info_dict = {}
			cur_certificate_info_dict['requirements'] = list(split[1:])
			requirement_list = []
			for requirement in cur_certificate_info_dict['requirements']:
				courses = requirement.split('|')
				requirement_list.extend(courses)
			cur_certificate_info_dict['requirement_set'] = set(requirement_list)

			certificate_name = split[0]
			self.certificate_requirements[certificate_name] = cur_certificate_info_dict

	def is_in_major_requirements(self, course_num, major):
		if not major:
			return False
		return course_num in self.major_requirements[major]['requirement_set']

	def is_in_certificate_requirements(self, course_num, certificate):
		#import pdb; pdb.set_trace()
		if not certificate:
			return False
		return course_num in self.certificate_requirements[certificate]['requirement_set']

	def check_all_major_requirements(self, courses, major):
		for course in courses:
			if course in self.major_requirements[major]['requirement_set']:
				return True
		return False

	def check_all_certificate_requirements(self, courses, certificate):
		for course in courses:
			if course in self.certificate_requirements[certificate]['requirement_set']:
				return True
		return False