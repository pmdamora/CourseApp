# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# This module decides everything that the user gets to see

from flask import render_template, jsonify, request, flash, redirect, url_for, make_response
from CourseApp import app, db
from flask.ext.user import login_required, current_user
from CourseApp.courses.models import Course
from CourseApp.users.models import User
from CourseApp.courses import viewfunctions
from CourseApp.config.settings import ITEMS_PER_PAGE
from CourseApp.courses import course_dict

# The error pages
# This includes 500,404,403,410 errors
@app.errorhandler(500)
def page_not_found(e):
    return render_template('/error_pages/500.html',title='Internal Server Error'), 500
  
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/error_pages/404.html',title='Page not found'), 404
  
    
@app.errorhandler(403)
def page_not_found(e):
    return render_template('/error_pages/403.html',title='Get out of here!'), 403
  
    
@app.errorhandler(410)
def page_not_found(e):
    return render_template('/error_pages/410.html',title='We lost it!'), 410


# The following few methods will be for JSON pages, aka pages the user never actually sees, but
# deliver us data
# If the route is prefaced by an underscore, it's for JSON/AJAX


# Gets all course arguments 
# Whenever an option is clicked in the sort bar, it goes through here
@app.route('/_course_args')
def course_args(page=1):
	
	# Get each argument and assign it to a variable
	# If it's of a "new" type then we add a comma so it can be easilly turned into a list late
    query = str(request.args.get('query'))
    
    old_s = str(request.args.get('old_s'))
    new_s = "," + str(request.args.get('new_s'))
    
    old_level = str(request.args.get('old_level'))
    new_level = ',' + str(request.args.get('new_level'))
    
    old_day = str(request.args.get('old_day'))
    new_day = ',' + str(request.args.get('new_day'))

    
    # First we're going to deal with subjects
    # s is the concatenation of the new subject and the old subjects
    # This variable is only for passing back to javascript
    s = old_s + new_s + ","
    
    # Create an array from the old_s string
    subject_list = viewfunctions.create_list(old_s)
    
    # Add the new_s to the end of the list we just creates
    subject_list.append(new_s.replace(",",""))
    
    # This is the simplest filter
    # Just make sure we only show subjects not in our subject_list
    if subject_list is not None:
    	subjects_filter = (~Course.subject.in_(subject_list))
    else:
    	subjects_filter = False
    	
    
    # Now we're dealing with the levels
    l = old_level[:-1] + new_level + ","
    
    # Same deal, create the list, append the new item
    level_list = viewfunctions.create_list(old_level)
    level_list.append(new_level.replace(",",""))
    
    # Creating the filter is more complicated so we pass our list to another method and get
    # the filter back
    levels_filter = viewfunctions.get_level_filters(level_list)
    
    
    # Now we're dealing with days
    d = old_day[:-1] + new_day + ","
    
    # Same deal, create the lsit, append the new item
    day_list = viewfunctions.create_list(old_day)
    day_list.append(new_day.replace(",",""))
    
    # We pass our list to another method and get our filter
    days_filter = viewfunctions.get_days_filters(day_list)
    
    # Now we need to get all of our filters together
    # Luckily we have a method to do that
    list_of_filters = viewfunctions.get_list_of_filters(subjects_filter,levels_filter,days_filter)
    
    
    # Check if we're on a page with a search query
    # If we are, add in that query as another filter
    # Otherwise just create the normal filter
    if(query != 'false'):
    	filter_fall14 = Course.query.filter(list_of_filters & (Course.title.like('%'+query+'%'))).paginate(page, ITEMS_PER_PAGE, False)
    else:
    	filter_fall14 = Course.query.filter(list_of_filters).paginate(page, ITEMS_PER_PAGE, False)

    
    # Render both courses.html and pagination.html
    # The pagination needs to be updated with the new number of pages
    rendered = render_template('courses.html',course=filter_fall14)
    pages = render_template('pagination.html',course=filter_fall14)
    
    # Return all of this in JSON format
    return jsonify(subjects=s,filtered_list=rendered,pagination=pages,levels=l,days=d)


# We want to be able to paginate via ajax
# This method does just that
# It's mostly a reproduction of course_args
# I'll probably combine them in optimization
@app.route('/_paginate')
def jquery_pagination():

    # Get each of the url parameters as variables
    query = str(request.args.get('query'))
	
    # We're including the page numbe this time around
    next_page = request.args.get('next_page',1, type=int)
    old_s = str(request.args.get('old_s'))
    old_level = str(request.args.get('old_level'))
    old_day = str(request.args.get('old_day'))
    
    # Agian we have to convert the subject_list into an actual list
    subject_list = viewfunctions.create_list(old_s)
    
    # And then create our filter
    if subject_list is not None:
    	subjects_filter = (~Course.subject.in_(subject_list))
    else:
    	subjects_filter = None 
    
    # Create the list of levels and get our filter
    level_list = viewfunctions.create_list(old_level)
    levels_filter = viewfunctions.get_level_filters(level_list)
    
    # Create the list of days and get our filter
    day_list = viewfunctions.create_list(old_day)
    days_filter = viewfunctions.get_days_filters(day_list)
    
    # Get the final list of ALL filters
    list_of_filters = viewfunctions.get_list_of_filters(subjects_filter,levels_filter,days_filter)

    
    # Check if there's a search query in play
    # If so, add it to our filters, otherwise, business as usual
    if(query != 'false'):
    	filter_fall14 = Course.query.filter(list_of_filters & (Course.title.like('%'+query+'%'))).paginate(next_page, ITEMS_PER_PAGE, False)
    else:
    	filter_fall14 = Course.query.filter(list_of_filters).paginate(next_page, ITEMS_PER_PAGE, False)

    # Render the html for pagination and courses
    pages = render_template('pagination.html',course=filter_fall14)
    rendered = render_template('courses.html',course=filter_fall14)
    
    # Return the JSON data
    return jsonify(filtered_list=rendered,pagination=pages)


# This function manages the user's worksheet
# It runs when there's an addition or subtraction from the user's worksheet
@app.route('/_worksheet')
def worksheet():
	
	# Get the crn they sent us
	crn = str(request.args.get('crn'))
	minus_crn = str(request.args.get('minus_crn'))
	
	# Find out who the current user is so we can get their worksheet
	this_user = User.query.get(current_user.id)
	
	# Check if there is a crn to add
	if(crn != 'False'):
	# Add the new item to their worksheet
		if(this_user.worksheet):
			this_user.worksheet = (this_user.worksheet + ',' + crn) 
		else:
			this_user.worksheet = (',' + crn) 
			
	# Otherwise we're removing a crn	
	else:
		minus_string = "," + minus_crn
		this_user.worksheet = str(this_user.worksheet).replace(minus_string,'')
		
	# Commit our chanes to the database
	db.session.commit()
		
	# Create the worksheet object
	worksheet = viewfunctions.create_worksheet(this_user.worksheet)
	
	# Set their worksheet to a variable
	current_ws = this_user.worksheet
	
	# Get the total credits
	total_credits = 0
	for course in worksheet:
		total_credits = total_credits + int(course.credits)
	
	# Render the new worksheet popup template
	worksheet = render_template('worksheet_popup.html', ws=current_ws, worksheet=worksheet, total_credits=total_credits)
	
	# Return the JSON data
	return jsonify(crn=current_ws,worksheet=worksheet)



# We're no longer dealing with JSON
# So everything here actually get displayed

# This method is for the search page
# We use the HTTP GET method
@app.route('/search',methods=['GET'])
@login_required
def search(page=1):

	# Get the search query from the url
	query = request.args['q']
	
	# Get the current user's worksheet
	this_user = User.query.get(current_user.id)
	
	# Create the worksheet object
	worksheet = viewfunctions.create_worksheet(this_user.worksheet)
	
	# Get the total credits
	total_credits = 0
	for course in worksheet:
		total_credits = total_credits + int(course.credits)
		
	# Create our filter, with the seach query
	# We only want to show courses with the query in the title
	fall14 = Course.query.filter(Course.title.like('%'+query+'%')).paginate(page, ITEMS_PER_PAGE, False)	
	course_list = course_dict.course_list
	
	# Return this as html
	# We still use index.html on the search page
	return render_template('index.html', title = 'Search Results for ' + query, course = fall14, course_list = course_list, query = query,worksheet = worksheet, ws = this_user.worksheet, total_credits = total_credits)


# The index page
# This is the homepage and just display a list of courses
@app.route('/')
@app.route('/index')
@login_required
def index(page=1):
	# Get the current user's worksheet
	this_user = User.query.get(current_user.id)
	
	# Create the worksheet object
	worksheet = viewfunctions.create_worksheet(this_user.worksheet)
	
	# Get the total credits
	total_credits = 0
	for course in worksheet:
		total_credits = total_credits + int(course.credits)
		
	# Create query of all courses
	fall14 = Course.query.paginate(page, ITEMS_PER_PAGE, False)
	course_list = course_dict.course_list
	
	# Return the rendered template
	return render_template('index.html',title = 'Home',course = fall14, course_list = course_list, worksheet = worksheet, ws = this_user.worksheet, total_credits = total_credits)



# The downloads
# Handles file generation and downloads
@app.route('/download/worksheet')
@login_required
def download_worksheet():
    # Get the current user's worksheet
    this_user = User.query.get(current_user.id)
	
    # Create the worksheet object
    worksheet = viewfunctions.create_worksheet(this_user.worksheet)
	
	# Create the CSV string
	# These are just the headers
    csv = "Course Title, Section Title, Time/Days Class Meets, Location, Professor, # Credits, CRN \n"
    
    # Loop through each item in the worksheet
    for item in worksheet:
        csv = csv + item.subject + " " + str(item.course_num) + "," + item.title + " - " + item.section + "," + item.start_time + "-" + item.end_time + " " + item.days + "," + item.building + " " + item.room + "," + item.instructor + "," + str(item.credits) + "," + item.crnumber + "\n"
	
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=worksheet.csv"
    return response
    

# The downloads
# Handles file generation and downloads
@app.route('/download/course/<crnumber>')
@login_required
def download_course(crnumber):
    # Get the course with this crn
    course = Course.query.filter_by(crnumber=crnumber).first()

    # Create the CSV string
	# These are just the headers
    csv = "Course Title, Section Title, Time/Days Class Meets, Location, Professor, # Credits, CRN \n"
    
    # Loop through each item in the worksheet
    csv = csv + course.subject + " " + str(course.course_num) + "," + course.title + " - " + course.section + "," + course.start_time + "-" + course.end_time + " " + course.days + "," + course.building + " " + course.room + "," + course.instructor + "," + str(course.credits) + "," + course.crnumber + "\n"
	
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=" + course.subject + "_" + str(course.course_num) + ".csv"
    return response


# The course page
# This page shows for any single course and takes a crn as an argument
@app.route('/course/<crnumber>')
@login_required
def courses(crnumber):
	# Get the current user's worksheet
	this_user = User.query.get(current_user.id)
	
	# Create the worksheet object
	worksheet = viewfunctions.create_worksheet(this_user.worksheet)
	
	# Get the total credits
	total_credits = 0
	for course in worksheet:
		total_credits = total_credits + int(course.credits)
	
	# Get the course with THIS crn
	this_course = Course.query.filter_by(crnumber=crnumber).first()
	title = this_course.title
	
	# Render the html template
	return render_template('course_single.html',title=title,course=this_course, worksheet = worksheet, ws = this_user.worksheet, total_credits = total_credits)	


# The about page
@app.route('/about')
def about():
	return render_template('about.html',title='About')
	

# The user profile page
# Only viewable by that user
@app.route('/user/profile')
@login_required
def user_profile_page():
	
	# We're actually overriding flask-user here
	return render_template('/users/user_profile.html',title='My Account')

# The worksheet page
# Shows the worksheet on its own page, rather than a popup
@app.route('/user/worksheet')
@login_required
def full_worksheet():
	# We're actually overriding flask-user here
	return render_template('/users/user_profile.html',title='My Account')
