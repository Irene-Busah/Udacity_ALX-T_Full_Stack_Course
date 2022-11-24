import sqlite3
from flask import Flask, request, jsonify, abort


app = Flask(__name__)

# dummy test data
books = [{
	'id': 1,
	'title': 'A Fire Upon the Deep',
	'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'
}, {
		'id': 2,
		'title': 'The Ones Who Walk Away From Omelas',
		'author': 'Ursula K. Le Guin',
		'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
		'published': '1973'},
	 {
		'id': 3,
		'title': 'Dhalgren',
		'author': 'Samuel R. Delany',
		'first_sentence': 'to wound the autumnal city.',
		'published': '1975'
	 }
]

def dict_factory(cursor, row):
	dictionary = {}
	for idx, col in enumerate(cursor.description):
		dictionary[col[0]] = row[idx]
	return dictionary



# home page route
@app.route('/', methods=['GET'])
def index():
	return '<h1>Distant Reading Archive</h1> <p>This is a prototype API for distant reading of science fiction novels</p>'

# retrieves all the books
@app.route('/v1/resources/books/all', methods=['GET'])
def retrieve_books():
	# error = False
	# connecting to the database: SQLite
	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	
	books = cur.execute('SELECT * FROM books;').fetchall()
	return jsonify(books)
	

# retrieve a specific book
@app.route('/v1/resources/books', methods=['GET'])
def retrieve_specific_book():
	query_parameters = request.args

	id = query_parameters.get('id')
	published = query_parameters.get('published')
	author = query_parameters.get('author')

	query = "SELECT * FROM books WHERE"
	to_filter = []

	if id:
		query += ' id=? AND'
		to_filter.append(id)
	if published:
		query += ' published=? AND'
		to_filter.append(published)
	if author:
		query += ' author=? AND'
		to_filter.append(author)
	if not (id or published or author):
		return page_not_found(404)

	query = query[:-4] + ';'

	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()

	results = cur.execute(query, to_filter).fetchall()

	return jsonify(results)

# handling errors
@app.errorhandler(404)
def page_not_found(error):
	return jsonify({
		'success': False,
		'Error': 404,
		'Message': 'Page not found: The resource could not be found'
	}), 404

# runs the flask application
if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=5000)
