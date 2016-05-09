import numpy as np

class Planner(object):
	major_type_col = 0
	major_col = 1
	def __init__(self, majors_filename, certificates_filename, course_id_to_num):
		self.major_requirements = {}
		self.certificate_requirements = {}
		self.major_membership_matrix = None
		self.certificate_membership_matrix = None
		self.id_to_num = course_id_to_num
		self.course_num_list = self.id_to_num.values()

		self._process_major_requirements(majors_filename)
		self._process_certificate_requirements(certificates_filename)
		self._build_major_membership_matrix()
		self._build_certificate_membership_matrix()

		self.major_row_dict = {}
		for i, major in enumerate(self.major_requirements.keys()):
			self.major_row_dict[major] = i

		self.certificate_row_dict = {}
		for i, certificate in enumerate(self.certificate_requirements.keys()):
			self.certificate_row_dict[certificate] = i

		# self.course_num_col_dict = {}
		# for i, course_num in enumerate(self.course_num_list):
		# 	self.course_num_col_dict[course_num] = i

	def _process_major_requirements(self, majors_filename):
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

	def _process_certificate_requirements(self, certificates_filename):
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
		try:
			if course_num in self.major_requirements[major]['requirement_set']:
				return True
		except TypeError:
			import pdb; pdb.set_trace()
		wild_course = course_num[:4]+'*'
		return wild_course in self.major_requirements[major]['requirement_set']


	def is_in_certificate_requirements(self, course_num, certificate):
		if not certificate:
			return False
		if course_num in self.certificate_requirements[major]['requirement_set']:
			return True
		wild_course = course_num[:4]+'*'
		return wild_course in self.certificate_requirements[major]['requirement_set']

	def _build_major_membership_matrix(self):
		self.major_membership_matrix = np.zeros((len(self.major_requirements), len(self.course_num_list)))
		for i, major in enumerate(self.major_requirements.keys()):
			for j, course_num in enumerate(self.course_num_list):
				major_membership_matrix[i,j] = self.is_in_major_requirements(course_num, major)

	def _build_certificate_membership_matrix(self):
		self.certificate_membership_matrix = np.zeros((len(self.certificate_requirements), len(self.course_num_list)))
		for i, certificate in enumerate(self.certificate_requirements.keys()):
			for j, course_num in enumerate(self.course_num_list):
				major_membership_matrix[i,j] = self.is_in_certificate_requirements(course_num, certificate)

	def get_major_boost_vector(self, major):
		return self.major_membership_matrix[self.major_row_dict[major], :]

	def get_certificate_boost_vector(self, certificate):
		return self.certificate_membership_matrix[self.certificate_row_dict[certificate], :]

	def get_course_num(self, course_id):
		return self.id_to_num[course_id]
