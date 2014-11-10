from pyfaces import main


def recog(image):

	match = main(image, 'path_to_folder_with_friends_pictures')
	filepath = str(match[0])
	id_start = (filepath.find("(") + 1)
	id_end = filepath.find(")", id_start)
	fb_id_number = filepath[id_start:id_end]

	return fb_id_number