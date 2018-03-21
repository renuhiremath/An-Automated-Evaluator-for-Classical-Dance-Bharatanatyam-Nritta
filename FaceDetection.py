import numpy as np
import cv2
import sys
import glob
import os
import sqlite3

face_coordinates_list = list()

def face_detect_main(eval_id,input_folder, results_folder):
	img_list = []

	face_coordinates_list = list()

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()
	
	rows = cur.execute("select * from image_list where eval_id = "+ str(eval_id) )
	for row in rows:
		img_list.append(input_folder + "\\" +row[1])

	cur.close()

	if not os.path.exists(results_folder):
		os.makedirs(results_folder)
		print "Creating folder " + results_folder

	print "Face Detection started..."
	cl = ["haarcascade_profileface.xml","haarcascade_frontalface_alt.xml","haarcascade_frontalface_alt2.xml","haarcascade_frontalface_default.xml"]
		
	
	total_frames = len(img_list)

	for f in range(1,total_frames+1):
		i = input_folder + "\\" + "frame" + str(f) + ".jpg" 

		img = cv2.imread(i)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		
		iname, fx, fy, nx, ny = ["", 0,0,0,0]
		if (face_coordinates_list!=[]):
			iname, fx, fy, nx, ny=face_coordinates_list[len(face_coordinates_list)-1]
		
		for c in cl:
			classifier = cv2.CascadeClassifier("haarxmls\\"+c)
			detected = False
			faces = classifier.detectMultiScale(gray)
			
			if faces != ():
				faces = sorted(faces, key=lambda x: x[3])
				final_coordinates = [0,0,0,0]
				detected_face = False
				
				height, width ,c  = img.shape

				hh = 0.04*height
				ww = 0.06*width

				for (x,y,w,h) in faces:
					if ((face_coordinates_list==[] or (abs(int(x+(w/2)) - fx) <=ww and abs(int(y+(h/2)) - fy) <=hh)) and final_coordinates[3] < h):
						final_coordinates = [x,y,w,h] 
						detected_face = True

				if (detected_face == True):
					print ".",
					x,y,w,h = final_coordinates
					img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),4)
					img = cv2.circle(img,(x+(w/2),y+(h/2)),2,(255,255,255),4)
					img = cv2.circle(img,(x+(w/2),y+h+25),2,(255,255,255),4)
					cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
					face_coordinates_list.append([i.split('\\')[1],(x+(w/2)),(y+(h/2)),(x+(w/2)),(y+h+25)])
					img_list.remove(i)
					break
		
		if (i in img_list):
			print ".",
			face_coordinates_list.append([i.split('\\')[1],fx, fy, nx, ny])
			
			img = cv2.circle(img,(fx,fy),2,(255,255,255),4)
			img = cv2.circle(img,(nx,ny),2,(255,255,255),4)
			cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
			img_list.remove(i)

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()
	for i in face_coordinates_list:
		n,x1,y1,x2,y2 = i
		x1 = int(x1)
		y1 = int(y1)
		x2 = int(x2)
		y2 = int(y2)
		cur.execute("insert into joint_details_face values(?,?,?,?,?,?)",[eval_id,n,x1,y1,x2,y2])
	cur.close()
	print "\nCompleted Face Detection..."
	print