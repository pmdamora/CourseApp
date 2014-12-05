# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Queries database information
# Contains functions for course viewing filters

from CourseApp.courses.models import Course
from CourseApp.users.models import User
from flask import url_for 
from flask.ext.user import current_user
import xlwt

# Takes a string with comma deliminators as an argument and return that string as a list of item
def create_list(old_s):
    s_list = []
        
    old_list = old_s.split(",")
    for item in old_list:
	s_list.append(item)
    return s_list
	
# Creates the exact filter for course levels
# Takes a list of option as an argument and returns a levels_filter
def get_level_filters(level_list):
 	
    # Parentheses matter quite a lot here
    # For now we have a messy series of if statements
    # I'll re-do this in optimization
    levels_filter = None
    if "0-99" in level_list:
    	if(levels_filter is None):
    	    levels_filter = (Course.course_num > 100)
    	else:
    	    levels_filter = ((Course.course_num > 100) & levels_filter)

    if "100-199" in level_list:
    	if(levels_filter is None):
    	    levels_filter = ((Course.course_num > 199) | (Course.course_num < 100))
    	else:
    	    levels_filter = (((Course.course_num > 199) | (Course.course_num < 100)) & levels_filter)
    		
    if "200-299" in level_list:
    	if(levels_filter is None):
    	    levels_filter = ((Course.course_num > 299) | (Course.course_num < 200))
    	else:
    	    levels_filter = (((Course.course_num > 299) | (Course.course_num < 200)) & levels_filter)
    if "300+" in level_list:
    	if(levels_filter is None):
    	    levels_filter = (Course.course_num < 300)
    	else:
    	    levels_filter = ((Course.course_num < 300) & levels_filter)
    
    if levels_filter is not None:
    	return levels_filter
    else:
    	return False

# Creates the filters for days
# Takes a list of day option as an argument
def get_days_filters(day_list):
 	
    # Again, parentheses matter here
    days_filter = False
    
    print day_list
    
    for day in day_list:
    	if day != '':
	    if days_filter is not False:
	        days_filter = ((~Course.days.like('%'+day+'%')) & days_filter)
	    else:
	    	days_filter = (~Course.days.like('%'+day+'%'))
    		
    return days_filter
    	

# Compiles filters of multiple types into a big filter we can actually pass into our query
# Returns a list_of_filters	
def get_list_of_filters(subjects_filter,levels_filter,days_filter):
    list_of_filters = None
    templist = [subjects_filter, levels_filter, days_filter]
    are_filters = False
	
    # Check each type of filter in our list
    for item in templist:
        # The filter must actually contain data, otherwise there is no filter
	# and we can move on to the next item
	if item is not False:
			
	    # Check if our flag for whether list_of_filters is empty is true
	    # Yes, we could just check if list_of_filter is empty, but this is for
	    # Syntaxically readable
	    if are_filters:
		list_of_filters = ((item) & list_of_filters)
	    else:
		list_of_filters = item
		are_filters = True
			
    return list_of_filters		
		
def create_worksheet(this_user):
    # Split the query into a list
    # This creates a list of objects, we want a list of strings
    ws = str(this_user).split(',')
	
    # So let's make a string out of it
    sheet = ''
    for item in ws:
        if sheet != '':
	    sheet = sheet + "," + item
	else:
	    sheet = item
	
    # And now create a list again
    ws = sheet.split(',')	
	
    # And create the query
    worksheet = Course.query.filter(Course.crnumber.in_(ws)).all()
	
    return worksheet
	

def worksheet_to_excel(this_user):
    # Create the query to work with
    worksheet = create_worksheet(this_user)
	
    # Create a workbook
    book = xlwt.Workbook()
    sh = book.add_sheet("Sheet 1")
    
    # Write the title to the worksheet
    sh.write(0, 0, "My Worksheet")
    
    book.save(url_for('static', filename='excel/worksheet.xls'))
    
    
	
	
	
	
	
	
	
	
	
	