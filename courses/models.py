# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# Defines the DataSort class and methods
# Defines Course db model
# Defines the WebScraper class and methods

import urllib2
import requests
import time
from bs4 import BeautifulSoup
from CourseApp import db

# The database model for Course
# Each course will contain all of these fields
# The table is created with this structure in root __init__.py   
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(10), nullable=False, default=False)
    course_num = db.Column(db.Integer, nullable=False, default=False)
    title = db.Column(db.String(255), nullable=False, default=False)
    crnumber = db.Column(db.String(25), nullable=False, default=False)
    section = db.Column(db.String(10),nullable=True,default=False)
    section_type = db.Column(db.String(10),nullable=True,default=False)
    code = db.Column(db.String(10),nullable=True,default=False)
    max_enroll = db.Column(db.Integer,nullable=True,default=False)
    current_enroll = db.Column(db.Integer,nullable=True,default=False)   
    start_time = db.Column(db.String(25),nullable=True,default=False)
    end_time = db.Column(db.String(25),nullable=True,default=False)
    days = db.Column(db.String(25),nullable=True,default=False)
    credits = db.Column(db.String(10),nullable=True,default=False)
    building = db.Column(db.String(25),nullable=True,default=False)
    room = db.Column(db.String(25),nullable=True,default=False)
    instructor = db.Column(db.String(255),nullable=True,default=False)
    instructor_netid = db.Column(db.String(255),nullable=True,default=False)
    instructor_email = db.Column(db.String(255),nullable=True,default=False) 
    description = db.Column(db.UnicodeText(),nullable=True,default=False)
    
    # Initializes the value set when a new course is added
    def __init__(self, subject, course_num, title, crnumber, section, section_type, code, max_enroll, current_enroll, start_time, end_time, days, credits, building, room, instructor, instructor_netid, instructor_email,description):
        self.subject = subject
        self.course_num = course_num
        self.title = title
        self.crnumber = crnumber
        self.section = section
        self.section_type = section_type
        self.code = code  
        self.max_enroll = max_enroll
        self.current_enroll = current_enroll
        self.start_time = start_time
        self.end_time = end_time
        self.days = days
        self.credits = credits
        self.building = building
        self.room = room
        self.instructor = instructor
        self.instructor_netid = instructor_netid
        self.instructor_email = instructor_email
        self.description = description

# Contains a description and a CRN
class Description(db.Model):   
	id = db.Column(db.Integer, primary_key=True)
	crnumber = db.Column(db.String(25), nullable=False, default=False)
	description = db.Column(db.UnicodeText(),nullable=True,default=False)
	
	def __init__(self, crnumber, description):
		self.crnumber = crnumber
		self.description = description
	

# This class is for sorting through data taken from UVM before it is added to 
# our databse
class DataSort:

	# Takes a target_url as an argument
	# Only called in schedule.py
	def	__init__(self,target_url):
		self.target_url = target_url
		
	# Downloads the file from the internet and returns the data
	# Note: In the future use requests over urllib2 for consistency
	def downloadFile(self,target_url):
		data = urllib2.urlopen(target_url)
		return data 
				
	# Sort the file data into a list of item
	# Remove excess quotes and commas
	# Return the sorted list
	def sortFile(self,data):
		dataList = []
		data.next() ## skip the first line
		for line in data:
			lineList = line.split('","')		
			
			for item in lineList:
				dataList.append(item.replace('"',''))
		return dataList
			    	
	# The main method, only this method should be called publicly
	# Calls the downloadFile method, sortFile method,
	# and adds each course to the database with its data
	def addCourses(self):
		data = self.downloadFile(self.target_url)
		
		dataList = self.sortFile(data)
		i = 0
		while i+17 < len(dataList):
			instructor = dataList[i+15].split(',')
			instructor_name = instructor[1] + " " + instructor[0]
			
			course = Course(dataList[i],dataList[i+1],dataList[i+2],dataList[i+3],dataList[i+4],dataList[i+5],dataList[i+6],dataList[i+7],dataList[i+8],dataList[i+9],dataList[i+10],dataList[i+11].replace(" ",""),dataList[i+12],dataList[i+13],dataList[i+14],instructor_name,dataList[i+16],dataList[i+17],'')
			db.session.add(course)
			i+=18
		db.session.commit()



# This class contains all methods necessary for parsing html
class WebScraper:
	
	# Takes a target url as an argument
	def	__init__(self,target_url):
		self.target_url = target_url
	
	# Downloads the html of the page
	# Will try max_attempts times in case network is spotty	
	def get_page(self,url,max_attempts):
		for i in xrange(max_attempts):
			r = requests.get(url)
			if r.status_code == 200:
				return r.content
		print r.status_code
		return False
    
	# Using bs4, parses the course description text from the html page
	def get_course_description(self,url):
		html = self.get_page(url,5)
		
		if html:
			soup=BeautifulSoup(html)
			
			# First we need the article#uvmmaincontent tag
			uvmmain=soup.find(id="uvmmaincontent")
			
			# Then we get the SECOND p child
			description = uvmmain.findChildren('p')[1]
			
			# The p child contains a span that we don't want
			# So we extract it
			[s.extract() for s in description.find('span')]
			
			# Finally grab the actual text of description and return it
			description = description.text
			return description
		else:
			return False
	
	# Query's all the items in the Course database and loops through each one, getting its description
	def add_description(self):
		courses = Course.query.all()
		i = 1		
		
		# Loop through each course	
		for c in courses:
			
			# The url is a combination of the target_url and the crn of this course
			url = self.target_url + c.crnumber
			description = self.get_course_description(url)
			
			c.description = description
			db.session.commit()
			
			# If we were successful, print the number we're on and a success message
			print str(i) + "Success!"
			i += 1
			
			# UVM throttles the connection if we work too fast
			# I'll need to find a way around that, but for now time.sleep() works
			time.sleep(3)
	