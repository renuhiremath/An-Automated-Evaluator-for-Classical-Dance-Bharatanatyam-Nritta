import cv2
import sys
import os
import sqlite3

def convert_video_to_frames(user_name,video_path,results,video_name,resize_factor = 1.0):
	"""extracting frames from the video"""
	print "Processing video : ",video_path
	print "Converting it into frames..."

	vidcap = cv2.VideoCapture(video_path)
	vidcap.set(cv2.CAP_PROP_POS_MSEC,100)
	success,image = vidcap.read()
	
	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()

	cur.execute("insert into user_list (user_name,video_type) values(?,?)",[user_name,video_name])

	row = cur.execute("select max(eval_id) from user_list")
	eval_id = 0
	for r in row:
		eval_id = r[0]
	results = user_name+"_"+str(video_name)+"_"+str(eval_id)
	if not os.path.exists(results):
		os.makedirs(results)
		print "Creating folder " + results
	
	t=100
	transpose_image = False

	length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
	width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps    = vidcap.get(cv2.CAP_PROP_FPS)

	print "Width :",width
	print "Height :",height
	sec = length / fps * 1000
	print "Length (in sec):",int(sec/1000)
	
	if (height<width):
		print "saving transpose of the images"
		transpose_image = True

	while success and t<sec:
		if (transpose_image):
			image = cv2.transpose(image)
			image = cv2.flip(image,1)

		image_name = "frame" + str(t/100) + ".jpg"
		cv2.imwrite( results + "\\" + "frame" + str(t/100) + "_original.jpg", image)
		cv2.imwrite( results + "\\" + image_name, image)
		cur.execute("insert into image_list values(?,?,?)",[eval_id,image_name,-1])
		t+=100
		vidcap.set(cv2.CAP_PROP_POS_MSEC,t)
		success,image = vidcap.read()
	con.close()
	print "\nFrames stored in " + results + " folder"
	return eval_id

if __name__=="__main__":
	#convert_video_to_frames("bhat","videos\\shreya\\d1.mp4","d1",1)
	#convert_video_to_frames("bhat","videos\\shreya\\dd.mp4","d2",2)
	#convert_video_to_frames("bhat","videos\\shreya\\d33.mp4","d3",3)
	#convert_video_to_frames("bhat","videos\\shreya\\d4.mp4","d4",4)
	#convert_video_to_frames("bhat","videos\\shreya\\d5.mp4","d5",5)
	#convert_video_to_frames("sam","videos\\samhitha\\dance1.mp4","dance1",1)
	print