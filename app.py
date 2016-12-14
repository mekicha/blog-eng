from datetime import datetime
from flask import Flask, request, redirect
from flask import url_for, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = True

db = SQLAlchemy(app)

class Post(db.Model):
	id = db.Column('post_id', db.Integer, primary_key = True)
	title = db.Column(db.String())
	body = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)

	def __init__(self, title, body, pub_date=None):
		self.title = title
		self.body = body
		if pub_date is None:
			pub_date = datetime.utcnow()
		self.pub_date = pub_date

	def __repr__(self):
		return '<title, body {} {}>'.format(self.title, self.body)

@app.route('/')
def index():
	"""
	Query the database and render all the posts on the page
	"""
	posts = Post.query.order_by(Post.pub_date.desc()).all()
	return render_template('index.html', posts=posts)

@app.route('/newpost', methods=['GET','POST'])
def newpost():
	"""
	Run form validation.
	Create a new post.
	Save to the database.
	Redirect user to the post.
	"""
	error = None;
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		if not title or not body:
			error = 'Please fill in title and post body'
			return render_template('new.html', error=error)
		else:
			new_post = Post(title, body)
			db.session.add(new_post)
			db.session.commit()
			post = Post.query.order_by(Post.pub_date.desc()).first()
			return redirect(url_for('single_post', id=post.id))

			



		return render_template(url_for('index'))
	return render_template('new.html')
	

@app.route('/posts/<int:id>')
def single_post(id):
	"""
	Return and render a single post by its id.
	"""
	post = Post.query.filter_by(id=id).first_or_404()
	return render_template('single_post.html', post=post)



if __name__ == '__main__':
	app.run(debug=True)