""" Flask app files for FlaskFeedback Project stores passwords with Bcrypt"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, connect_db, db
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def home():
    """Redirect to register page"""
    return redirect("/register")

@app.route("/register", methods=["GET","POST"])
def register_user():
    """Register User by adding them to db and redirect to secret page"""
    
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    form = RegisterForm()

    if form.validate_on_submit():
        username  = form.username.data 
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user= User.register(username,pwd,email,first_name,last_name)

        db.session.add(user)
        try: 
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username Taken')
        
        session["username"] = user.username
        
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login',methods=["GET","POST"])
def login_user():
    """log the user in"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")


    form = LoginForm() 
    if form.validate_on_submit():
        username  = form.username.data 
        pwd = form.password.data

        user = User.authenticate(username,pwd)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else: 
            form.username.errors = ["Bad name or password"]
    return render_template("login.html",form=form)
    

@app.route('/users/<username>')
def show_user_info(username):
    """Return Secret Content for Logged in Users"""
    if "username" not in session:
        flash("You must be logged in to view that page!")
        return redirect('/')
    else:
        user= User.query.get_or_404(username)
        form = DeleteForm()
        return render_template('user_details.html', user=user, form=form)

@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def add_user_feedback(username):
    """Show add feedback form and process"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title,content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('feedback_form.html', form = form)

@app.route('/users/<username>/delete',methods=["POST"])
def delete_user(username):
    """delete a user account and associated feedback"""
    user = User.query.get_or_404(username)
    if "username" not in session or session["username"] != user.username:
        raise Unauthorized()
    session.pop("username")
    db.session.delete(user)
    db.session.commit()
    return redirect('/')




@app.route('/feedback/<int:feedback_id>/update', methods=["GET","POST"])
def edit_user_feedback(feedback_id):
    """Show edit user feedback form and process"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or session["username"] != feedback.username:
        raise Unauthorized()
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('/edit_feedback.html',form=form)

@app.route('/feedback/<int:feedback_id>/delete',methods=["POST"])
def delete_user_feedback(feedback_id):
    """delete users feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or session["username"] != feedback.username:
        raise Unauthorized()
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')


@app.route('/logout')
def logout_user():
    session.pop("username")
    return redirect('/')