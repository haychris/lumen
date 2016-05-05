from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query')
def process_query():
	query = request.args.get('query')
	print 'Query: ', query
	return render_template('queryResult.html')

@app.route('/userratings')
def get_user_ratings():
	return render_template('courseHistInput.html')

@app.route('/recommend')
def process_recommendations():
	return render_template('courseHistResult.html')


if __name__ == '__main__':
    app.run(debug=True)
