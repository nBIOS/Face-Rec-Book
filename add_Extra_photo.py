import datetime

def addExtra(user, fb_id_number, image):

	time = datetime.datetime.now()

	image.save("users/" + user + "/cgr/resized(%d)_(%s).jpg" %(fb_id_number, time))

	return "Image saved to your database."

