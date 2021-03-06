from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Length(min=5, max=64), DataRequired(), Email(message='invalid email')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, max=128, message='password need to be 8 to 128 characters')])
    remember_me = BooleanField('Keep me logged in', default=False)
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Nickname', validators=[Length(min=4, max=25), DataRequired()])
    email = StringField('Email Address', validators=[Length(min=5, max=64), DataRequired(), Email()])
    password = PasswordField('New Password',
                             validators=[Length(min=8, max=128), DataRequired(),
                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class UploadForm(FlaskForm):
    file = FileField('new_file', validators=[validators.input_required()])
