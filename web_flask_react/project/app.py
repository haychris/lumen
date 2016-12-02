import os
import cPickle as pickle

from flask import Flask, render_template
from flask import request
from flask import url_for
from flask import redirect

from flask_cas import CAS
from flask_cas import login_required


from course import CourseRenderer
from recommend import Recommender
from search import Searcher
from planner import Planner

app = Flask(__name__)
app.secret_key = 'my super secret key is the most secret ever'
app.config['SECRET_KEY'] = 'my super secret key is the most secret ever'
cas = CAS(app)
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
# app.config['CAS_SERVER'] = 'https://signon.cs.princeton.edu/'
app.config['CAS_AFTER_LOGIN'] = ''
app.config['SESSION_TYPE'] = 'filesystem'

filename = os.path.join(os.getcwd(), 'project/static/necessities.pickle')
course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k, vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_info_dict, course_association_dictionary, pagerank_dict = pickle.load(
    open(filename, 'rb'))

planner = Planner(
    os.path.join(os.getcwd(), 'project/static/majors.csv'),
    os.path.join(os.getcwd(), 'project/static/certificates.csv'),
    course_id_list, class_number_lookup_dict, pagerank_dict)
recommender = Recommender(course_id_lookup_dict, class_number_lookup_dict,
                          course_cluster_probs_dict, k, course_id_list,
                          planner)
searcher = Searcher(vectorizer, tfidf_mat, word_dict, course_doc_dict,
                    course_id_list, course_id_lookup_dict,
                    class_number_lookup_dict, planner)
course_renderer = CourseRenderer(course_info_dict, planner)

max_results = 20


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query')
@login_required
def process_query():
    try:
        major = request.cookies['Major']
        certificate = request.cookies['Certificate']
    except KeyError:
        major = ''
        certificate = ''
    query = request.args.get('query')
    if not query:
        return redirect(url_for('/'))
    print 'Query: ', query
    terms = query.lower().split()
    results = searcher.search(query.lower(), major, certificate)
    courses = [
        course_renderer.get_course(course_id)
        for course_id in results[:max_results]
    ]
    return render_template(
        'queryResult.html',
        results=courses,
        terms=terms,
        major=major,
        certificate=certificate)


@app.route('/userratings')
@login_required
def get_user_ratings():
    return render_template('courseHistInput.html')


@app.route('/recommend')
@login_required
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
    recommendations = recommender.recommend(courses, ratings, major,
                                            certificate)
    courses = [
        course_renderer.get_course(course_id)
        for course_id in recommendations[:max_results]
    ]
    return render_template(
        'courseHistResult.html',
        results=courses,
        major=major,
        certificate=certificate)


if __name__ == '__main__':
    app.run(debug=True)
