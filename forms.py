from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

class RegistrationForm(FlaskForm):
    Fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    Mname = StringField('Middle Name', validators=[DataRequired(), Length(min=1, max=255)])
    Lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=255)])
    age = IntegerField('Age', validators=[DataRequired()])
    contact_num = StringField('Contact Number', validators=[DataRequired(), Length(min=1, max=255)])
    dateofbirth = DateField('Date of birth', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=255)])
    role = SelectField('Role', validators=[InputRequired()], choices=[('1', 'Admin'), ('2', 'Employee')])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=10, max=255), EqualTo('password')])
    submit = SubmitField('Register')
    update = SubmitField('Update')

class LoginForm(FlaskForm):
    Lusername = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    Lpassword = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=255)])
    Lsubmit = SubmitField('Login')

class CustomerForm(FlaskForm):
    Fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    Mname = StringField('Middle Name', validators=[DataRequired(), Length(min=1, max=255)])
    Lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=255)])
    contact_num = StringField('Contact Number', validators=[DataRequired(), Length(min=1, max=255)])
    dateofbirth = DateField('Date of birth', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=255)])
    amount = IntegerField('Loan Amount', validators=[DataRequired()])
    mode = SelectField('Payment Mode', validators=[InputRequired()], choices=[('1', 'ATM')])
    rate = SelectField('Rate', validators=[InputRequired()], choices=[('1', '1 Year'), ('2', '2 Years')])
    c_Fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    c_Mname = StringField('Middle Name', validators=[DataRequired(), Length(min=1, max=255)])
    c_Lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    c_contact_num = StringField('Contact Number', validators=[DataRequired(), Length(min=1, max=255)])
    c_address = StringField('Address', validators=[DataRequired(), Length(min=1, max=255)])
    contract = FileField('Contract', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Register')
    update = SubmitField('Update')

class LoanStatus(FlaskForm):
    emp_id = StringField('Lender Employee ID', validators=[DataRequired(), Length(min=1, max=10)])
    cus_id = StringField('Customer ID', validators=[DataRequired(), Length(min=1, max=10)])