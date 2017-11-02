from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    email = StringField('email', validators=[Length(min=5, max=50), DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
"""
class UploadForm(Form):
    file = FileField()
"""

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[Length(min=6, max=35), DataRequired()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
