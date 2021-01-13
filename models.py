from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

"""Models for flaskFeedback Project"""


db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable = False, unique=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    feedback = db.relationship("Feedback",backref='user', cascade="all, delete")

    #register 
    @classmethod
    def register(cls,username,pwd,email,first_name,last_name):
        """Register User with hashed passsword and return user object"""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)

    #authenticate
    @classmethod
    def authenticate(cls,username,pwd):
        """Authenticate user and return user or False"""
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,pwd):

            return user
        else: 
            return False

class Feedback(db.Model):
    """Model for feedback from users"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
