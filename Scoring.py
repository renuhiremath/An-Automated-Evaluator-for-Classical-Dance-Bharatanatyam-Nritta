import sqlite3
from operator import itemgetter
import matplotlib.pyplot as plt

def score(user_name,video_type):

	con = sqlite3.connect("dance_eval.db",isolation_level=None)
	cur = con.cursor()

	row = cur.execute("select eval_id from user_list where user_name = '"+user_name+"' and video_type = "+str(video_type))
	eval_id = 0
	for r in row:
		eval_id = r[0]

	l=cur.execute("select * from image_list where eval_id="+str(eval_id)).fetchall()
	m=cur.execute("select * from joint_details_face where eval_id="+str(eval_id)).fetchall()
	n=cur.execute("select * from joint_details_upperbody where eval_id="+str(eval_id)).fetchall()
	o=cur.execute("select * from joint_details_lowerbody where eval_id="+str(eval_id)).fetchall()
	p=cur.execute("select * from upperbody_posture where eval_id="+str(eval_id)).fetchall()

	ld=[]
	#sorted(s,key=itemgetter(1))
	m.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	o.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	n.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	p.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))

	#neck added to list
	for elem in m:
		k=[]
		for i in range(2, len(elem)):	
			k.append(elem[i])
		ld.append(k)
	#upper body added to list
	j=0
	for elem in n:
		for i in range(2, len(elem)):
			ld[j].append(elem[i])
		j=j+1
	j=0
	for elem in o:
		for i in range(2,len(elem)):
			ld[j].append(elem[i])
		j=j+1
	j=0
	for elem in p:
		for i in range(2,len(elem)):
			ld[j].append(elem[i])
		j=j+1

	row = cur.execute("select eval_id from user_list where user_name = 'bhat' and video_type = "+str(video_type))
	eval_id = 0
	for r in row:
		eval_id = r[0]

	l=cur.execute("select * from image_list where eval_id="+str(eval_id)).fetchall()
	m=cur.execute("select * from joint_details_face where eval_id="+str(eval_id)).fetchall()
	n=cur.execute("select * from joint_details_upperbody where eval_id="+str(eval_id)).fetchall()
	o=cur.execute("select * from joint_details_lowerbody where eval_id="+str(eval_id)).fetchall()
	p=cur.execute("select * from upperbody_posture where eval_id="+str(eval_id)).fetchall()

	con.close()
	lt=[]
	#sorted(s,key=itemgetter(1))
	m.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	o.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	n.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	p.sort(key=lambda x:int(x[1].split('e')[1].split('.')[0]))
	#neck added to list
	for elem in m:
		k=[]
		for i in range(2, len(elem)):	
			k.append(elem[i])
			
		lt.append(k)
	#upper body added to list
	j=0
	for elem in n:
		for i in range(2, len(elem)):
			lt[j].append(elem[i])
		j=j+1
	j=0
	for elem in o:
		for i in range(2,len(elem)):
			lt[j].append(elem[i])
		j=j+1
		if (j==len(lt)):
			break
	j=0
	for elem in p:
		for i in range(2,len(elem)):
			lt[j].append(elem[i])
		j=j+1
		if (j==len(lt)):
			break

	no_of_frames = min(len(ld),len(lt))

	score = 0
	score_up = 0
	score_low = 0
	upper_neg=0
	lower_neg=0
	hand_Score=0


	frame_no = []
	score_final = []

	for i in range(0,len(ld)):
		
		if(i == no_of_frames-2):
			break

		l1=ld[i]
		l2=lt[i]
		l11=ld[i+1]
		l22=lt[i+1]

		f_score_cum = 0
		f_score_upper = 0
		f_score_lower = 0
		for k in range(0,len(ld[i])-1):
				
			x = l11[k]-l1[k]
			y = l22[k]-l2[k]
			f_score =0
			#print x,y
			if(((x<y+10 and x>y-10) or x==y) and (x*y>=0)):
				f_score = 10
				if (k>=0 and k<=7):
					f_score_upper = f_score_upper+f_score
				else:
					f_score_lower = f_score_lower+f_score
			elif(((x<y+15 and x>y-15) or x==y) and (x*y>=0)):
				f_score=5
				if (k>=0 and k<=7):
					f_score_upper = f_score_upper+f_score
				else:
					f_score_lower = f_score_lower+f_score
			
			elif (((x<y+20 and x>y-20) or x==y)and (x*y>=0)):
				f_score =3
				if (k>=0 and k<=7):
					f_score_upper = f_score_upper+f_score
				else:
					f_score_lower = f_score_lower+f_score		
			else:
				if (k>=0 and k<=7):
					upper_neg = upper_neg+1
				else:
					lower_neg = lower_neg+1
				#print "probs!", 
				#print "frame" + str(i+1) +".jpg",
			f_score_cum = f_score_cum+f_score 
		if(l22[len(ld[i])-1] != "unknown" and l11[len(ld[i])-1] == l22[len(ld[i])-1]):
			h_score = 10
		else:
			h_score = 0
		f_score_cum = f_score_cum+f_score+h_score
		hand_Score = hand_Score+h_score	
		score_up = score_up + f_score_upper
		score_low = score_low + f_score_lower
		score = score + f_score_cum
		score_final.append(f_score_cum/17.0)

	report_card = []

	print "overall score on 10: ",((float(score_up)/(8*no_of_frames))+float((score_low)/(8*no_of_frames))+(float(hand_Score)/(no_of_frames)))/3 
	report_card.append("Overall Score : " + str(((float(score_up)/(8*no_of_frames))+float((score_low)/(8*no_of_frames))+(float(hand_Score)/(no_of_frames)))/3) + " out of 10")
	print "upper body score on 10: ", float(score_up)/(8*no_of_frames)
	report_card.append("Upperbody Score : " + str( float(score_up)/(8*no_of_frames)) + " out of 10")
	print "lower body score on 10: ", float(score_low)/(8*no_of_frames)
	report_card.append("Lowerbody Score : " + str( float(score_low)/(8*no_of_frames)) + " out of 10")
	print "Hand gestures score 10: ", float(hand_Score)/(no_of_frames)
	report_card.append("Hand gestures Score : " + str( float(hand_Score)/(no_of_frames)) + " out of 10")

	if(float(score_up)/(8*no_of_frames) < 5):
		print "Weak Upper body. Have to improve on your upper body postures"
		report_card.append("Weak Upper body. Have to improve on your upper body postures")
	elif (float(score_up)/(8*no_of_frames) > 5 and float(score_up)/(8*no_of_frames) < 7):
		print "Average Upper body. Just need a little more practice to perfect things! "
		report_card.append("Average Upper body. Just need a little more practice to perfect things! ")
	else:
		print "Great Upper body postures. Keep up the good work!"
		report_card.append("Great Upper body postures. Keep up the good work!")

	if(float(score_low)/(8*no_of_frames) < 5):
		print "Weak Lower body. Have to improve on your lower body postures"
		report_card.append("Weak Lower body. Have to improve on your lower body postures")
	elif (float(score_low)/(8*no_of_frames) > 5 and float(score_low)/(8*no_of_frames) < 7):
		print "Average Lower body. Just need a little more practice to perfect things! "
		report_card.append("Average Lower body. Just need a little more practice to perfect things! ")
	else:
		print "Great Lower body postures. Keep up the good work!"
		report_card.append("Great Lower body postures. Keep up the good work!")
	if(float(hand_Score)/(no_of_frames) < 5):
		print "Weak Hand gestures. Have to improve on your hastas"
		report_card.append("Weak Hand gestures. Have to improve on your hastas")
	elif (float(hand_Score)/(no_of_frames) > 5 and float(hand_Score)/(no_of_frames) < 7):
		print "Average hand gestures. Just need a little more practice to perfect things! "
		report_card.append("Average hand gestures. Just need a little more practice to perfect things! ")
	else:
		print "Great hand gestures. Keep up the good work!"
		report_card.append("Great hand gestures. Keep up the good work!")

	
	f = 1
	for f in range(1,len(score_final)+1):
		frame_no.append(f)
		f+=1

	#print len(score_final), len(frame_no)

	
	report_card.append(frame_no)
	report_card.append(score_final)
	return report_card

if __name__ =="__main__":
	#print score("sam",1)
	print