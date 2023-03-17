from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import email_validator

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired('Email is required.'), 
        Email('Email is not valid.'),
        Length(min=5, max=255, message='Email has wrong length.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required.'),
        Length(min=6, max=255, message='Password has wrong length.')
    ])
    submit = SubmitField('Login')
