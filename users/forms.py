# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Defines Custom forms for use with flask-user
# Instantiated in root __init__.py

from flask.ext.user.forms import RegisterForm
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, validators

# Our custom registration form
# Here we can add extra fields besides the default for flask-user
class MyRegistrationForm(RegisterForm):
	
	# We want to get the user's first name
    first_name = StringField('First Name', validators=[validators.Required('First Name is required')])
