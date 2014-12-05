# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Initiates the app
# There's some circular imports in here, which is generally bad practice
# But flask likes it, so be careful

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter
from CourseApp.users.forms import MyRegistrationForm

# Initialize app config setting
app = Flask(__name__)
app.config.from_object('CourseApp.config.settings')
app.jinja_env.add_extension('jinja2.ext.do')

# Initialize Flask extensions
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
mail = Mail(app)                                # Initialize Flask-Mail

# Import models
from CourseApp.users import models
from CourseApp.courses.models import Course

# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, models.User)        # Register the User model
user_manager = UserManager(db_adapter, app, register_form=MyRegistrationForm)     # Initialize Flask-User

# Import views
from CourseApp.pages import views
