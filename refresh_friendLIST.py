# -*- coding: utf-8 -*-
"""
@author: Callum Kift and Ralph Harti
"""

# Refresh friend list - only downloads name and ID of friends, not their P-file-P

import facebook
import os
import authentication

def refreshFriends(user, token):

	graph = facebook.GraphAPI(token) # Allows access to profile
	friends = graph.get_connections(user, "friends") # Retrieves friends list

	if os.path.exists("photos/"+user+"/.friends_list.txt"): # check to see if there is an old token and deletes if there is one
		os.remove("photos/"+user+"/.friends_list.txt")

	friendList_file = open ("photos/"+user+"/.friends_list.txt", "w+r")
	friendList_file = open ("photos/"+user+"/.friends_list.txt", "a")
	for friend in friends['data']:
		friendList_file.write("%s, %s\n" %(friend['name'].encode('utf-8'), friend['id']))
		print friend['name']
	friendList_file.close()

	return "Friend list has been refreshed"