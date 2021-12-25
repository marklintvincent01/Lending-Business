from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField
from wtforms.fields.simple import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    Fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    Mname = StringField('Middle Name', validators=[DataRequired(), Length(min=1, max=255)])
    Lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=255)])
    contact_num = StringField('Contact Number', validators=[DataRequired(), Length(min=1, max=255)])
    dateofbirth = DateField('Date of birth', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=255)])
    validID = FileField('Valid ID', validators=[FileAllowed(['jpg', 'png'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=10, max=255), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=255)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    