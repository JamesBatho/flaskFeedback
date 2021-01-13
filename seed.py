"""Seed file to make sample data for pets db."""

from models import db, User, Feedback
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Feedback.query.delete()


# Add users and posts
john = User(username="John",password="123",email="24",first_name="12a",last_name="123")

# Add new objects to session, so they'll persist
db.session.add(john)


#have to add users first to not violate foreign key constraints
db.session.commit()

feed = Feedback(title="test",content="alsdkjf",username="John")

db.session.add(feed)


# Commit--otherwise, this never gets saved!
db.session.commit()
