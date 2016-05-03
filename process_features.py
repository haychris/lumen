import sys
from collections import defaultdict

f = open(sys.argv[1])
header = f.readline()
column_keys = header.replace('\n', '').split(',')
# column_keys = termid,courseid,title,all_listings_string,area,prereqs,descrip

		
class_dict = defaultdict(lambda : defaultdict(lambda: defaultdict(list)))
for line in f:
	line = line.replace('\n', '').replace('"', '')
	line_dict = {column_keys[i]:val for i, val in enumerate(line.split(','))}
	cur_term_dict = class_dict[line_dict["termid"]]
	cur_course_dict = cur_term_dict[str(int(line_dict["courseid"]))]
	cur_course_dict["all_listings_string"] = line_dict["all_listings_string"]
	cur_course_dict["area"] = line_dict["area"]
	cur_course_dict["title"] = line_dict["title"]
	cur_course_dict["prereqs"] = line_dict["prereqs"]
	cur_course_dict["descrip"] = line_dict["descrip"]
