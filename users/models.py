# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Defines the User() model

from flask.ext.user import UserMixin
from CourseApp import db

# Here we define the database model for User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    password = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    
    # Extra model fields
    first_name = db.Column(db.String(50), nullable=False, default='')

    # Worksheet
    worksheet = db.Column(db.String(255), nullable=True, default='')