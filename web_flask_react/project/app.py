import os
from flask import Flask, render_template
from flask import request
from flask import url_for

from course import Course, CourseRenderer
from recommend import Recommender
from search import Searcher
from planner import Planner

app = Flask(__name__)

import cPickle as pickle

filename = os.path.join(os.getcwd(), 'project/static/website_necessities.pickle')
course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k, vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_info_dict, course_association_dictionary, pagerank_dict = pickle.load(open(filename, 'rb'))

planner = Planner(os.path.join(os.getcwd(),'project/static/majors.csv'), os.path.join(os.getcwd(),'project/static/certificates.csv'), course_id_list, class_number_lookup_dict, pagerank_dict)
recommender = Recommender(course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k, course_id_list, planner)
searcher = Searcher(vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_id_lookup_dict, class_number_lookup_dict, planner)
course_renderer = CourseRenderer(course_info_dict, planner)
# recommender = Recommender(os.path.join(os.getcwd(), 'project/static/recommender_necessities.pickle'))
# searcher = Searcher(os.path.join(os.getcwd(), 'project/static/search_necessities.pickle'), recommender.course_id_lookup_dict)
# planner = Planner(os.path.join(os.getcwd(),'project/static/majors.csv'), os.path.join(os.getcwd(),'project/static/certificates.csv'), searcher.course_id_list, recommender.class_number_lookup_dict)
# searcher.add_planner(planner)

# course_renderer = CourseRenderer(os.path.join(os.getcwd(),'project/static/course_info_necessities.pickle'), planner)

max_results = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query')
def process_query():
	try:
		major = request.cookies['Major']
		certificate = request.cookies['Certificate']
	except KeyError:
		major = ''
		certificate = ''
	query = request.args.get('query')
	print 'Query: ', query
	terms = query.lower().split()
	results = searcher.search(query.lower(), major, certificate)
	courses = [course_renderer.get_course(course_id) for course_id in results[:max_results]]
	return render_template('queryResult.html', results=courses, terms=terms, major=major, certificate=certificate)

@app.route('/userratings')
def get_user_ratings():
	return render_template('courseHistInput.html')

@app.route('/recommend')
def process_recommendations():
	print request.cookies
	major = request.cookies['Major']
	certificate = request.cookies['Certificate']
	courses = []
	ratings = []
	for entry in request.cookies['CourseInfo'].split('|'):
		split = entry.split(':')
		courses.append(split[1].split(',')[0].replace(' ', '').upper())
		ratings.append(int(split[-1]))
	# import pdb; pdb.set_trace()	
	print courses
	print ratings
	recommendations = recommender.recommend(courses, ratings, major, certificate)
	courses = [course_renderer.get_course(course_id) for course_id in recommendations[:max_results]]
	return render_template('courseHistResult.html', results=courses, major=major, certificate=certificate)

if __name__ == '__main__':
    app.run(debug=True)

