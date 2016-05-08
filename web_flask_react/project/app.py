import os
from flask import Flask, render_template
from flask import request
from flask import url_for

from course import Course, CourseRenderer
from recommend import Recommender
from search import Searcher

app = Flask(__name__)

recommender = Recommender(os.path.join(os.getcwd(), 'project/static/recommender_necessities.pickle'))
#searcher = Searcher(os.path.join(os.getcwd(), 'project/static/search_necessities.pickle'))
course_renderer = CourseRenderer(os.path.join(os.getcwd(),'project/static/course_info_necessities.pickle'))

max_results = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query')
def process_query():
	query = request.args.get('query')
	print 'Query: ', query
	terms = query.lower().split()
	results = searcher.search(terms)
	courses = [course_renderer.get_course(course_id) for course_id in results[:max_results]]
	return render_template('queryResult.html', results=courses, terms=terms)

@app.route('/userratings')
def get_user_ratings():
	return render_template('courseHistInput.html')

@app.route('/recommend')
def process_recommendations():
	courses = []
	ratings = []
	for entry in request.cookies['CourseInfo'].split('|'):
		split = entry.split(':')
		courses.append(split[1].split(',')[0].replace(' ', '').upper())
		ratings.append(int(split[-1]))
	# import pdb; pdb.set_trace()	
	print courses
	print ratings
	recommendations = recommender.recommend(courses, ratings)
	courses = [course_renderer.get_course(course_id) for course_id, rating in recommendations[:max_results]]
	return render_template('courseHistResult.html', results=courses)

if __name__ == '__main__':
    app.run(debug=True)

