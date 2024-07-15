from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserRegistrationForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from secret import FLASK_SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_exercise"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET","POST"])
def register_user():

    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template("register.html", form=form)
        session["username"] = new_user.username
        flash("Account created! Welcome!", "success")
        return redirect('/secret')

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user_info(username):
    if 'username' not in session:
        flash("Please log in first!", "danger")
        return redirect('/login')
    elif (session['username'] != username):
        flash("You are not authorized to view the requested page")
        return redirect('/')
    else:
        user = User.query.filter_by(username=username).first()
        feedback = Feedback.query.filter_by(username=username).all()
        return render_template("show_user.html", user=user, feedback=feedback)
    
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if 'username' not in session:
        flash("Please log in first!", "danger")
        return redirect('/login') 
    
    if (session['username'] != username):
        flash("You are not authorized to view the requested page")
        return redirect('/')
        
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback.add_feedback(title, content, username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    
    else:
        user = User.query.filter_by(username=username).first()
        return render_template("add_feedback.html", user=user, form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    user = User.query.filter_by(username=username).first()

    if 'username' not in session:
        flash("Please log in first!", "danger")
        return redirect('/login') 
    
    if (session['username'] != username):
        flash("You are not authorized to view the requested page")
        return redirect('/')
        
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    
    else:
        return render_template("edit_feedback.html", user=user, form=form, feedback=feedback)
    

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    if 'username' not in session:
        flash("Please log in first!", "danger")
        return redirect('/login') 
    
    if (session['username'] != username):
        flash("You are not authorized to view the requested page")
        return redirect('/')
    
    else:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted")
        user = User.query.filter_by(username=username).first()
        all_feedback = Feedback.query.filter_by(username=username).all()
        return render_template("show_user.html", user=user,feedback=all_feedback)
    
@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')