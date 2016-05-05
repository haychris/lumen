from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query')
def hello():
	query = request.args.get('query')
	print query
	return render_template('queryResult.html')


if __name__ == '__main__':
    app.run(debug=True)
