# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Settings and configuration for courseapp

import os 

WTF_CSRF_ENABLED = True
SECRET_KEY = '###'

# Sets up SQLAlchemy database for DigitalOcean MySQL
SQLALCHEMY_DATABASE_URI = '###' # Password here, remove if public

# Configure Flask-Mail -- Required for Confirm email and Forgot password features
MAIL_USERNAME       = os.getenv('MAIL_USERNAME', '##')
MAIL_PASSWORD       = os.getenv('MAIL_PASSWORD', '##') # Password here, remove if public
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"CourseApp" <noreply@courseapp.me>')
MAIL_SERVER         = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT           = int(os.getenv('MAIL_PORT', '465'))
MAIL_USE_SSL        = os.getenv('MAIL_USE_SSL', True)

# Configure Flask-User
USER_ENABLE_CHANGE_USERNAME    = False
USER_ENABLE_USERNAME           = False
USER_APP_NAME                    = 'CourseApp'   # Used by email templates 

# Pagination
ITEMS_PER_PAGE = 20