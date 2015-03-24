from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField, validators
from models import db, User

class SignupForm(Form):
	firstname = StringField("First Name", validators=[validators.Required("First Name")])
	lastname = StringField("Last Name", validators=[validators.Required("Last Name")])
	email = StringField("Email", validators=[validators.Required("Email Address")])
	password = PasswordField("Password", validators=[validators.Required("Choose a Password")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query().filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken.")
			return False
		else:
			return True

class LoginForm(Form):
    username = StringField('username', validators=[validators.DataRequired()])
    password = StringField('password', validators=[validators.DataRequired()])
    email = StringField('email', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)