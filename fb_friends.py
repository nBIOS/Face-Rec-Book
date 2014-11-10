# -*- coding: utf-8 -*-
"""
@author: Callum Kift and Ralph Harti
"""

# This script finds all of the user's Facebook friends and downloads their friends' profile picture

import facebook
from fbconsole import graph_url
from urllib import urlretrieve
import os
import cv2
import Image
import numpy as np
import authentication
import shutil #used to delete excess folders and content at the end.

face_cascade = cv2.CascadeClassifier('opencv/opencv-2.4.8/data/haarcascades/haarcascade_frontalface_alt.xml')	# path tp cascade classifier

user = ""
files = ['username.txt']
for file in files: # Gets username from file
	with open( file, 'r' ) as f :     
        for line in f:
			line = line.strip()    
			user = line

if not os.path.exists("users/"+user): #creates user folder
			os.makedirs("users/"+user)

if os.path.exists("users/"+user+"/.fb_access_token"): # check to see if there is an old token and deletes if there is one
	os.remove("users/"+user+"/.fb_access_token")

# AUTHENTICATION OF USER - START
token = authentication.AUTHENTICATE()
# AUTHENTICATION OF USER - END
graph = facebook.GraphAPI(token) # Allows access to profile

friends = graph.get_connections(user, "friends") # Retrieves friends list

count = 0 #coutns number of facebook friends

if not os.path.exists("users/"+user+"/.friends_list.txt"):
	for friend in friends[data]: #Loops over friend list
		count += 1
		newpath = r"users/"+user+"/meta/%s" %friend['id'] #define path of where excess pics will be saved
		cgr_path = r"users/"+user+"/cgr" #defines path to where the final pics will be saved

		if not os.path.exists(newpath): #checks to see if already have path to friends' excess pics
			os.makedirs(newpath) #if not then makes it
			profile_pic = graph_url(str('/'+friend['id']+'/picture'), {"type":"large"})  # define the URL of the person's large profile picture you want to download
		 	urlretrieve(profile_pic, newpath+'/profile_picture(%s).jpg'%friend['id']) #Downloads the facebook picture and saves it 

		if not os.path.exists(cgr_path):
			os.makedirs(cgr_path) #creates path to final pics if not already there

		filename = newpath+'/profile_picture(%s).jpg'%friend['id'] #defines the variable as the friends pfilep
		print count, friend['id'], friend['name']
		img = cv2.imread(filename) 					# define test image, i.e. friends pfilep
		
		try:										# This just tests to see if the picture is viable - only isn't if there is no profile pic
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			detects = 0 #This is for if multiple faces are detected in the profile pic
			#crop = 0
			for (x,y,w,h) in faces:
				#crop += 1
				detects += 1
				#cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),0)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = img[y:y+h, x:x+w]
				#im = Image.open('test.jpg')
				crop_img = img[y:y+h, x:x+h]
				cv2.imwrite(newpath+'/cropped(%s)_(%d).jpg' %(friend['id'], detects), crop_img )
				gray = np.mean(crop_img, -1)
				cv2.imwrite(newpath+'/cropped_gray(%s)_(%d).jpg'  %(friend['id'], detects), gray)
			   
				width = 60
				height = 60
				gray_im = Image.open(newpath+'/cropped_gray(%s)_(%d).jpg'  %(friend['id'], detects))
				resized = gray_im.resize((width, height), Image.NEAREST)

				resized.save(cgr_path+'/resized(%s)_(%d).jpg'  %(friend['id'], detects))
		except cv2.error:
			pass
			
	friendList_file = open ("users/"+user"/.friends_list.txt", "w+r")
	friendList_file = open ("users/"+user"/.friends_list.txt", "a")
	for friend in friends['data']:
		friendList_file.write("%s, %s\n" %(friend['name'].encode('utf-8'), friend['id']))
	friendList_file.close()

	shutil.rmtree("users/"+user+"/meta") #deletes excess files at the end
else:
	print "already have this users data"