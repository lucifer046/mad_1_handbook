import sqlalchemy
# create_engine: Establishes a connection to the database (SQLite in this case)
from sqlalchemy import create_engine
# Table, Column, Integer, String, ForeignKey: Used to define the schema/structure of our database tables
from sqlalchemy import Table, Column, Integer, String, ForeignKey
# select: Used for constructing SQL SELECT statements (though we use session.query here)
from sqlalchemy import select

# Session: Manages the 'conversation' with the database, handling transactions and object state
from sqlalchemy.orm import Session
# declarative_base: A factory function that constructs a base class for declarative class definitions
from sqlalchemy.orm import declarative_base
# relationship: Defines a relationship between two mapped classes (e.g., User and Article)
from sqlalchemy.orm import relationship

# Base class for all models to inherit from
Base = declarative_base()

# Define the User model (represents the 'user' table)
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

# Define the Article model (represents the 'article' table)
class Article(Base):
    __tablename__ = 'article'
    article_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    # Define a many-to-many relationship with User through the junction table
    authors = relationship("User", secondary="article_authors")

# Junction table for many-to-many relationship between User and Article
class ArticleAuthors(Base):
    __tablename__ = 'article_authors'
    user_id = Column(Integer,   ForeignKey("user.user_id"), primary_key=True, nullable=False)
    article_id = Column(Integer,  ForeignKey("article.article_id"), primary_key=True, nullable=False) 

# Create the SQLite engine
eng = create_engine("sqlite:///./testdb.sqlite3") # eng: database_engine

if __name__ == '__main__':
    # Using a session to interact with the database
    with Session(eng, autoflush=False) as sess: # sess: database_session
        sess.begin()
        try:
            # Fetch existing users from the database
            # u1, u2: user_objects
            u1 = sess.query(User).filter(User.username == "thejeshgn").one()
            u2 = sess.query(User).filter(User.username == "raj").one()

            # Create a new Article instance
            art = Article(title="2nd Using relationship", content="2nd Use relationships to insert. It's easy") # art: article_object

            # Link authors to the article (SQLAlchemy handles the junction table insertion automatically)
            art.authors.append(u1)
            art.authors.append(u2)
            
            # Add the article to the session
            sess.add(art)
        except:
            # If something goes wrong, roll back any changes
            print("Exception occurred during database operation, rolling back...")
            sess.rollback()
            raise
        else:
            # If everything is successful, commit the transaction
            print("Data added successfully, committing transaction...")
            sess.commit()   

















