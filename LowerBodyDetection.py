import numpy as np
import cv2
import sys
import glob
import os
import sqlite3

lb_coordinates_list = list()

def lowerbody_detect_main(eval_id,input_folder, results_folder):
	img_list = []

	face_coordinates_list = list()
	lb_coordinates_list = list()

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

	print "Lowerbody Detection started..."
	cl = ["lower.xml"]
	
	total_frames = len(img_list)

	for f in range(1,total_frames+1):
		i = input_folder + "\\" + "frame" + str(f) + ".jpg" 

		img = cv2.imread(i)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)
		
		height, weight ,c  = img.shape

		iname, hiprx, hipry, hiplx, hiply, krx,kry, klx,kly = ["", 0,0,0,0,0,0,0,0]
		if (lb_coordinates_list!=[]):
			iname, hiprx, hipry, hiplx, hiply, krx,kry, klx,kly=lb_coordinates_list[len(lb_coordinates_list)-1]
			#print 
			#print "Old value :", shrx,shry, i
		
		for c in cl:
			classifier = cv2.CascadeClassifier("haarxmls\\"+c)
			detected = False
			lowerbody = classifier.detectMultiScale(gray)
			
			if lowerbody != ():
				lowerbody = sorted(lowerbody, key=lambda x: -x[3])
				final_coordinates = [0,0,0,0]
				detected_lb = False

				for (x,y,w,h) in lowerbody:
					#img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
					#print "After subtraction : ", shx-shrx, shy-shry
					if (final_coordinates[3] < h and y > height/2):
						final_coordinates = [x,y,w,h] 
						detected_lb = True
						#print "here :)"

				if (detected_lb == True):
					print ".",
					x,y,w,h = final_coordinates
					img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),4)
					img = cv2.circle(img,(x+int(w*1.0/3),y),2,(255,255,255),4)
					img = cv2.circle(img,(x+int(w*2.0/3),y),2,(255,255,255),4)
					facey = face_coordinates_list[f-1][2]
					if (facey < (0.35*height)):#35 per cent
						img = cv2.circle(img,(x+int(w*1.0/3),y+int(h/2)),2,(255,255,255),4)
						img = cv2.circle(img,(x+int(w*2.0/3),y+int(h/2)),2,(255,255,255),4)
						lb_coordinates_list.append([i.split('\\')[1],x+int(w*1.0/3),y,x+int(w*2.0/3),y,x+int(w*1.0/3),y+int(h/2),x+int(w*2.0/3),y+int(h/2)])
					elif (facey < (0.55*height)): # 55 per cent
						img = cv2.circle(img,(x+int(w*1.0/5),y+int(h/2)),2,(255,255,255),4)
						img = cv2.circle(img,(x+int(w*4.0/5),y+int(h/2)),2,(255,255,255),4)
						lb_coordinates_list.append([i.split('\\')[1],x+int(w*1.0/3),y,x+int(w*2.0/3),y,x+int(w*1.0/5),y+int(h/2),x+int(w*4.0/5),y+int(h/2)])
					else:
						img = cv2.circle(img,(x,y+int(h/2)),2,(255,255,255),4)
						img = cv2.circle(img,(x+w,y+int(h/2)),2,(255,255,255),4)
						lb_coordinates_list.append([i.split('\\')[1],x+int(w*1.0/3),y,x+int(w*2.0/3),y,x,y+int(h/2),x+w,y+int(h/2)])
					
					cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
					img_list.remove(i)
					break
		#if ub not found
		if (i in img_list):
			print ".",
			lb_coordinates_list.append([i.split('\\')[1],hiprx, hipry, hiplx, hiply, krx,kry, klx,kly])
			#print "Values : ",shrx,shry
			img = cv2.circle(img,(hiprx,hipry),2,(255,255,255),4)
			img = cv2.circle(img,(hiplx,hiply),2,(255,255,255),4)
			img = cv2.circle(img,(krx,kry),2,(255,255,255),4)
			img = cv2.circle(img,(klx,kly),2,(255,255,255),4)
			cv2.imwrite(results_folder+ "\\" + i.split('\\')[1],img)
			img_list.remove(i)

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()
	for i in lb_coordinates_list:
		n,x1,y1,x2,y2,x3,y3,x4,y4 = i
		x1 = int(x1)
		y1 = int(y1)
		x2 = int(x2)
		y2 = int(y2)
		x3 = int(x3)
		y3 = int(y3)
		x4 = int(x4)
		y4 = int(y4)
		cur.execute("insert into joint_details_lowerbody values(?,?,?,?,?,?,?,?,?,?)",[eval_id,n,x1,y1,x2,y2,x3,y3,x4,y4])
	cur.close()
	print "\nCompleted Lowerbody Detection..."
	print

if (__name__ == "__main__"):
	"""eval_id = 1
	lowerbody_detect_main(eval_id,"d1", "r111")
	eval_id = 2
	lowerbody_detect_main(eval_id,"d2", "r222")
	eval_id = 3
				lowerbody_detect_main(eval_id,"r3", "r3")
				eval_id = 4
				lowerbody_detect_main(eval_id,"r4", "r4")
				eval_id = 5
				lowerbody_detect_main(eval_id,"r5", "r5")"""
	"""
	eval_id = 17
	lowerbody_detect_main(eval_id,"d3", "r61")
	"""