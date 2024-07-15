from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username required"), Length(max=20, message="Username must be less than 20 characters")])
    password = PasswordField("Password (8 character minimum, 30 character maximum)", validators=[InputRequired(message="Password required"), Length(min=8, message="Password must be at least 8 characters")])
    email = StringField("Email", validators=[InputRequired(), Email(message="Valid email address required"), Length(max=50, message="Email must be less than 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired(message="First name required"), Length(max=30, message="First name must be fewer than 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name required"), Length(max=30, message="Last name must be fewer than 30 characters")])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password required")])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=20, message="Title must be fewer than 100 characters")])
    content = TextAreaField("Content", validators=[InputRequired()])