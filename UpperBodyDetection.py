import numpy as np
import cv2
import sys
import glob
import os
import sqlite3
import math

ub_coordinates_list = list()
hand_gestures_list = list()

def contains_face(f,face_coordinates_list, x,y,w,h):
	i,fx,fy,nx,ny=face_coordinates_list[f]
	if (x<=fx and fx<=(x+w) and y<=fy and fy<=(y+h)):
		if (x<=nx and nx<=(x+w) and y<=ny and ny<=(y+h)+50):
			return True
	return False

def detect_hand_gesture(img,x,y,w,h):
	posture = "unknown"
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	value = (35, 35)
	blurred = cv2.GaussianBlur(grey, value, 0)
	_, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	i,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	max_area = -1
	for i in range(len(contours)):
		cnt=contours[i]
		area = cv2.contourArea(cnt)
		if(area>max_area):
			max_area=area
			ci=i
	cnt=contours[ci]
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
	hull = cv2.convexHull(cnt)
	drawing = np.zeros(img.shape,np.uint8)
	#cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
	#cv2.drawContours(drawing,[hull],0,(0,0,255),0)
	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	count_defects = 0
	#cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
		b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
		c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
		angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
		if angle <= 90:
			count_defects += 1
			#cv2.circle(img,far,1,[0,0,255],-1)
		#cv2.line(img,start,end,[0,255,0],2)
	if count_defects == 1:
		posture = "pos1"
		#cv2.putText(img,"pos1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	elif count_defects == 2:
		posture = "pos2"
		#cv2.putText(img, "pos2", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
	elif count_defects == 3:
		posture = "pos3"
		#cv2.putText(img,"pos3", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	elif count_defects == 4:
		posture = "pos4"
		#cv2.putText(img,"pos4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	else:
		posture = "pos5"
		#cv2.putText(img,"pos5", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	return posture

def upperbody_detect_main(eval_id,input_folder, results_folder):
	img_list = []

	face_coordinates_list = list()
	ub_coordinates_list = list()

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()
	
	rows = cur.execute("select * from joint_details_face where eval_id = "+ str(eval_id) )
	for row in rows:
		img_list.append(input_folder + "\\" +row[1])
		l = list(row)
		l.pop(0)
		face_coordinates_list.append(l)

	cur.close()

	if not os.path.exists(results_folder):
		os.makedirs(results_folder)
		print "Creating folder " + results_folder

	print "Upperbody Detection started..."
	cl = ["upper1.xml"]
	
	total_frames = len(img_list)

	for f in range(1,total_frames+1):
		i = input_folder + "\\" + "frame" + str(f) + ".jpg" 
		img = cv2.imread(i)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		posture = "unknown"
		iname, shrx, shry, shlx, shly = ["", 0,0,0,0]
		if (ub_coordinates_list!=[]):
			iname, shrx, shry, shlx, shly=ub_coordinates_list[len(ub_coordinates_list)-1]
			_,posture = hand_gestures_list[len(hand_gestures_list)-1]
			#print "Old value :", shrx,shry, i
		
		for c in cl:
			classifier = cv2.CascadeClassifier("haarxmls\\"+c)
			detected = False
			upperbody = classifier.detectMultiScale(gray)
			
			if upperbody != ():
				upperbody = sorted(upperbody, key=lambda x: -x[3])
				final_coordinates = [0,0,0,0]
				detected_ub = False

				for (x,y,w,h) in upperbody:
					#img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
					#print "After subtraction : ", shx-shrx, shy-shry
					if (final_coordinates[3] < h and contains_face(f-1,face_coordinates_list,x,y,w,h)):
						final_coordinates = [x,y,w,h] 
						detected_ub = True
						#print "here :)"

				if (detected_ub == True):
					print ".",
					x,y,w,h = final_coordinates
					img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),4)
					img = cv2.circle(img,(x+(w/5),y+h),2,(255,255,255),4)
					img = cv2.circle(img,(x+(4*w/5),y+h),2,(255,255,255),4)
					cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
					ub_coordinates_list.append([i.split('\\')[1],(x+(w/5)),(y+h),(x+(4*w/5)),(y+h)])
					posture = detect_hand_gesture(img,x,y,w,h)
					hand_gestures_list.append([i.split('\\')[1],posture])
					#con.execute("insert into joint_details_face values(?,?,?,?,?,?)",[user_name,i.split("\\")[1],int(x+(w/2)),int(y+(h/2)),int(x+(w/2)),int(y+h+25)])
					#con.execute("insert into upperbody_gesture values(?,?,?)",[user_name,i.split("\\")[1],posture])
					img_list.remove(i)
					break
		#if ub not found
		if (i in img_list):
			print ".",
			ub_coordinates_list.append([i.split('\\')[1],shrx, shry, shlx, shly])
			hand_gestures_list.append([i.split('\\')[1],posture])
			#print "Values : ",shrx,shry
			img = cv2.circle(img,(shrx,shry),2,(255,255,255),4)
			img = cv2.circle(img,(shlx,shly),2,(255,255,255),4)
			cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
			img_list.remove(i)

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()
	for i in ub_coordinates_list:
		n,x1,y1,x2,y2 = i
		x1 = int(x1)
		y1 = int(y1)
		x2 = int(x2)
		y2 = int(y2)
		cur.execute("insert into joint_details_upperbody values(?,?,?,?,?,?)",[eval_id,n,x1,y1,x2,y2])
	#print hand_gestures_list
	for i in hand_gestures_list:
		n,p = i
		#print n,p
		cur.execute("insert into upperbody_posture values(?,?,?)",[eval_id,n,p])
	cur.close()
	print "\nCompleted Upperbody Detection..."
	print
