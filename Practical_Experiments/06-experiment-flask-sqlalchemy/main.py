import os
# Flask: Core web framework
# render_template: Renders HTML files using Jinja2
# request: Handles incoming HTTP request data
from flask import Flask, render_template, request
# SQLAlchemy: The Flask extension that provides a wrapper for SQLAlchemy ORM
from flask_sqlalchemy import SQLAlchemy

# c_dir: current_directory_path
c_dir = os.path.abspath(os.path.dirname(__file__))

# f_app: flask_application_instance
f_app = Flask(__name__)
# Configure SQLite DB URI
f_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(c_dir, "testdb.sqlite3") 

# db: sqlalchemy_database_instance
db = SQLAlchemy()
db.init_app(f_app)
f_app.app_context().push()

# Model Definitions
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True) # u_id: user_id
    u_name = db.Column(db.String, unique=True) # u_name: username
    email = db.Column(db.String, unique=True)

class Article(db.Model):
    __tablename__ = 'article'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # a_id: article_id
    title = db.Column(db.String)
    content = db.Column(db.String)
    # authors: list of User objects
    authors = db.relationship("User", secondary="article_authors")

class ArticleAuthors(db.Model):
    __tablename__ = 'article_authors'
    u_id = db.Column(db.Integer, db.ForeignKey("user.u_id"), primary_key=True, nullable=False)
    a_id = db.Column(db.Integer, db.ForeignKey("article.a_id"), primary_key=True, nullable=False) 

# Routes
@f_app.route("/", methods=["GET", "POST"])
def list_articles():
    if request.method == "GET":
        # Fetch all articles from DB
        arts = Article.query.all() # arts: articles_list
        return render_template("articles.html", articles=arts)

@f_app.route("/articles_by/<username>", methods=["GET", "POST"])
def articles_by_author(username):
    if request.method == "GET":        
        # Filter articles by author's username
        arts = Article.query.filter(Article.authors.any(u_name=username))
        return render_template("articles_by_author.html", articles=arts)

if __name__ == '__main__':
    # Run the Flask app on all interfaces
    f_app.run(host='0.0.0.0', debug=True, port=8080)
















