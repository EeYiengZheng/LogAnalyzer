<<<<<<< HEAD
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField
=======
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

>>>>>>> 6c7cfa9956903366fbf075e87ca7304551607f58

class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
"""
class UploadForm(Form):
    file = FileField()
"""

<<<<<<< HEAD
=======

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25), DataRequired()])
    email = StringField('Email Address', validators=[Length(min=6, max=35), DataRequired()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])
>>>>>>> 6c7cfa9956903366fbf075e87ca7304551607f58
