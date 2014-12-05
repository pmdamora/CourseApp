# Copyright 2014 CourseApp.me All rights reserved
#
# Authors: Paul D'Amora
# run.py runs entirely independent of flask and courseapp as a whole
# it simply write schedule.py to crontab which will contain all periodic tasks

from plan import Plan

cron = Plan()

# Add this script to the cron object and run it every 10 minutes
#cron.script('schedule.py', every='10.minute')

# This file needs to be ran from the terminal
# cron.run takes a bunch of different options
if __name__ == '__main__':
    cron.run('write') # could be 'check', 'write', 'update', 'clear'