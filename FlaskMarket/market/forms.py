from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
	username = StringField(label='User Name:  ', validators=Length(min=2, max=30), validators=[DataRequired()])

	email_address = StringField(label='Email: ', validators=Length(min=2, max=50), validators=[DataRequired()])

	password1 = PasswordField(label='Password: ', validators=Length(min=6), validators=[DataRequired()])

	password2 = PasswordField(label='Confirm password: ', validators=EqualTo('password1'), validators=[DataRequired()])

	submit = SubmitField(label='Create Account')

