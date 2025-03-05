from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=15)])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')

class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])

class ResetPaswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=15)])
    remember = BooleanField(label='Remember Me')
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Change Password', validators=[DataRequired()])

class UpdateAccountForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[DataRequired(), Length(max=20)])
    lastname = StringField(label='Last Name ', validators=[DataRequired(), Length(max=20)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    picture = FileField(label="Update Account Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update Account')
