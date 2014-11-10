# -*- coding: utf-8 -*-
"""
@author: Callum Kift and Ralph Harti
"""

import datetime

def noMatchAdd(user, image, friend):
	
	time = datetime.datetime.now()
	friendID = ""
	friendLIST = []
	files = ["photos/" + user + "/.friends_list.txt"]

	for file in files :
		with open( file, 'r' ) as f :     
	        # Loop over lines and extract variables of interest
			for line in f:
				line = line.strip()    #makes a line into a string
				columns = line.split(", ") #splits the line at each space
				
				dictFRIENDS = {'name': str(columns[0]), 'id': str(columns[1])}
				friendLIST.append(dictFRIENDS)


	for friend in friendLIST:
		if friendName == friend['name']:
			friendID = friend['id']
			image.save("users/" + user + "/cgr/resized(%d)_(%s).jpg" %(friendID, time))
			break

	if friendID != "":
		return "Image saved to your database"
	else:
		return "Could not find a match. Check to see if the name is spelt correctly or that you have them as a Facebook friend."

