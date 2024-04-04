from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, EqualTo

class RegisterUserForm(FlaskForm):
    """Registers a new user"""

    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                           validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password",
                           validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    email = EmailField('Email Adress',
                        validators=[InputRequired()])
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    last_name = StringField('Last Name',
                             validators=[InputRequired()])
    

    def __repr__(self):
        return f'username: {self.username.data}, pwd: {self.password.data}, email: {self.email.data}, first: {self.first_name.data}, last: {self.last_name.data}'
    
class LoginUserForm(FlaskForm):
    """Used for a user to log back in"""

    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                           validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    """Add feedback"""

    title = StringField('Title',
                        validators=[InputRequired()])
    content = TextAreaField('Content',
                            validators=[InputRequired()])