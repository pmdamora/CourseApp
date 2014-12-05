#!/flask/bin/python
# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Drives method calls to periodic tasks

import os 
import sys
import logging
logging.basicConfig(stream=sys.stderr)

# We aren't in flask, so we need to add to the system path
sys.path.insert(0,"/var/www/CourseApp/")

from CourseApp.courses.models import DataSort, Course, WebScraper
from CourseApp import db


# Delete all rows in the Course table
Course.query.delete()
db.session.commit()

# Running the addCourses method adds all of the courses to the database again
# only with new information
# This URL cam be changed for a different semester
ds = DataSort("http://giraffe.uvm.edu/~rgweb/batch/curr_enroll_spring.txt")
ds.addCourses()

# Here we run the webscraper method which is similar to addCourses only it just gets descriptions
# This URL also needs to be changed for a different semester
# the form is ?term=YYYY01, 01 for Spring and 09 for Fall
ws = WebScraper('http://www.uvm.edu/academics/courses/?term=201501&crn=')
ws.add_description()
