import json
import sys

# Read in the json file for classes
input_file_name = sys.argv[1]
input_file = open(input_file_name)
json_data = json.load(input_file)

# For list entries in the json, concatenate all entries in the list, 
# separated by whatever separator is defined as
seperator = ' '
for class_data in json_data:
	class_data['prof_string'] = seperator.join([prof['name'] for prof in class_data['profs']])
	class_data['all_listings_string'] = seperator.join([listing['dept'] + ' ' + listing['number'] for listing in class_data['listings']])


# features = ['termid', 'courseid', 'title', 'prof_string', 'all_listings_string', 'area', 'prereqs', 'descrip']
features = ['termid', 'courseid', 'title', 'all_listings_string', 'area', 'prereqs', 'descrip']


##### CONSTRUCT FEATURES CSV ####
output_file_name = input_file_name.split('.')[0] + '_features.csv'
out_file = open(output_file_name, 'w')

def reformat_for_csv(out):
	"""Reformats a string to work in a csv."""
	out = out.replace('"', '\\"')
	out = out.replace(',', ' ')
	ascii_out = out.encode('utf-8')
	sanitized_string = '\"%s\"' % ascii_out 
	return sanitized_string

# Print out header
for feat in features[:-1]:
	out_file.write(feat + ',')
out_file.write(features[-1] + '\n')

# Print out each class as line in csv
for class_data in json_data:
	for feat_name in features[:-1]:
		out_file.write(reformat_for_csv(class_data[feat_name]))
		out_file.write(',')
	out_file.write(reformat_for_csv(class_data[features[-1]]))
	out_file.write('\n')