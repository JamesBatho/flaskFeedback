from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username",validators=[InputRequired()])

    password = PasswordField("Password",validators=[InputRequired()])
    
    email = StringField("Email", validators=[InputRequired()])

    first_name = StringField("First Name", validators=[InputRequired()])

    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging a user in"""

    username = StringField("Username",validators=[InputRequired()])

    password = PasswordField("Password",validators=[InputRequired()])
    
class DeleteForm(FlaskForm):
    """Delete Form to use in template"""

class FeedbackForm(FlaskForm):
    """Feedback Form for getting data from user"""
    title = StringField("Title", validators=[InputRequired()])

    content = StringField("Content", validators=[InputRequired()])
