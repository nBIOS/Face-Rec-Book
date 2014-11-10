# -*- coding: utf-8 -*-
"""
@author: Callum Kift and Ralph Harti
"""


import fbconsole
import re
import mmap
import json
import requests
import facebook
import datetime
import recognition
import authentication


def info(fb_id):
	result = ''
	result_post = ''
	# AUTHENTICATION OF USER - START
	token = authentication.AUTHENTICATE()
	
	# AUTHENTICATION OF USER - END
	
	graph = facebook.GraphAPI(token)
	
	name = str(fb_id)
	
	
	r = requests.get("https://graph.facebook.com/" + name + "/posts/" + '?access_token=' + token) # get the json file for the feed
	
	raw = json.loads(r.text)

   
	
	activity = ''
	activity_person = ''
	activity_link = ''
	
	
	today = datetime.datetime.now()
	two_weeks = 14              # 14 days for two weeks, because the time difference is now taken in days
	
	print '\n\n'
	
	if len(raw) > 1 :
		what = raw['data'][0] # Only get the first data entry, since we are only interested in that
	
		if ('story' in what):
			activity = raw['data'][0]['story'] #+ '\n' + raw['data'][0]['description']
			activity_person = raw['data'][0]['from']['name']
			updated_time_activity =  what['updated_time']
			if ('link' in what):
				activity_link = raw['data'][0]['link']
		elif ('message' in what):
			activity = raw['data'][0]['message']
			activity_person = raw['data'][0]['from']['name']
			updated_time_activity =  what['updated_time']
			if ('link' in what):
				activity_link = raw['data'][0]['link']
		elif ('picture' in what):
			activity = raw['data'][0]['picture']
			activity_person = raw['data'][0]['from']['name']
			updated_time_activity =  what['updated_time']
			if ('link' in what):
				activity_link = raw['data'][0]['link']
		activity_time = datetime.datetime.strptime(updated_time_activity,'%Y-%m-%dT%H:%M:%S+0000')
		act_time = str(activity_time)        
		
		delta = today - activity_time   
		if delta.days < two_weeks:               # taking the difference in days -> delta.days is an interger!
		
			if (activity != ''):
				
				result =  activity + ' Posted by ' + activity_person + ' Date: ' + updated_time_activity
#                print 'Latest activity:'
#                print activity, 'From', activity_person
#                print 'Date:', updated_time_activity
			if (activity_link != ''):
				#result = result + 'Click for link: ' + activity_link
				result_link = activity_link
				#print 'Click for link:', activity_link
		else:  
			result = 'No activity in the last two weeks. Last activity on ' + act_time
			result_link = ''
	else:
		result =  'No recorded activity.'
		result_link = ''
	
	total = 0 # Count for number of posts
	for post in fbconsole.iter_pages(graph.get_object('/'+name+'/feed')): # Iterates over the feed and retrieves posts  
		post_time = datetime.datetime.strptime(post['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')
		delta = today - post_time    
		if delta.days < two_weeks:          # taking the difference in days -> delta.days is an interger!
			if ('message' in post): # Makes sure it is a post and not a 'like', comment etc.
				total += 1
				if (post['message'] != result):
					result_post =  'Latest wall post: ' + post['updated_time'] + ' ' + post['message'] + ' ' + 'From ' +  post['from']['name'] 
					result_post_link =  post['link']
					#print post['updated_time'], '\n', post['message'], '\n' , 'From', post['from']['name'], '\n'# Prints posts
				if total > 0: break # Limits to three, change 2-> 4 if you want the last 5 posts etc.
		else:
			result_post =  'No wall posts in the last two weeks.'
			result_post_link = ''
			break    
   
	
	
	return (result, result_post, result_link, result_post_link)
