from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
	"""
	Query the database and render all the posts on the page
	"""
	pass

@app.route('/newpost')
def newpost():
	"""
	Run form validation.
	Create a new post.
	Save to the database.
	Redirect user to the post.
	"""
	pass

@app.route('/posts/:id')
def single_post(id):
	"""
	Return and render a single post by its id.
	"""
	pass