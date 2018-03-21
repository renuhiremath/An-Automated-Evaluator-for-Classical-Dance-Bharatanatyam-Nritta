import Tkinter
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import cv2
class PrintReportCard(Tkinter.Frame):
	def __init__(self,user_name, report_card,eval_id,video_type,parent=None):
		Tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.user_name = user_name
		self.report_card = report_card
		self.eval_id = eval_id
		self.video_type = video_type
		self.initUI()
		self.centerWindow()
		self.create_labels()
		
	def create_labels(self):
		label1=Tkinter.Label(self,text="Report Card",relief=Tkinter.FLAT)
		label1["padx"]=15
		label1["pady"]=15
		label1["font"]=("comic sans ms",20,"bold underline")
		label1.place(x=200,y=10)
		
		self.analyse_text = Tkinter.StringVar()
		self.analyse_text.set("Here is your result "+ self.user_name + "...\n")
		label2=Tkinter.Label(self,textvar=self.analyse_text,relief=Tkinter.FLAT,justify= Tkinter.LEFT)
		label2["padx"]=15
		label2["pady"]=15
		label2["font"]=("comic sans ms",10)
		label2.place(x=100,y=100)

		self.button2=Tkinter.Button(self,text="Exit")
		self.button2["padx"]=30
		self.button2["pady"]=10
		self.button2["relief"]=Tkinter.RIDGE
		self.button2["font"]=("comic sans ms",15)
		self.button2["command"]=self.done
		self.button2.place(x=500,y=450)

		score_final = self.report_card.pop()
		frame_no = self.report_card.pop()

		self.add_text("Scores : ")
		self.add_text(self.report_card[0])
		self.add_text(self.report_card[1])
		self.add_text(self.report_card[2])
		self.add_text(self.report_card[3])
		self.add_text("\nSuggestions : ")
		self.add_text(self.report_card[4])
		self.add_text(self.report_card[5])
		self.add_text(self.report_card[6])
		self.old_frame = 0
		results_folder = self.user_name+"_"+str(self.video_type)
		if 1: # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

			def onpick3(event):
				ind = int(event.ind[0])
				if self.old_frame != ind:
					self.old_frame = ind
					print 'frame name:', "frame"+str(frame_no[ind])+".jpg"#, score_final[ind]
					
					img = cv2.imread("bhat_"+str(self.video_type)+"_"+str(self.video_type)+"\\frame"+str(frame_no[ind])+".jpg")
					height, width = img.shape[:2]
					res = cv2.resize(img,(720/2, 1280/2), interpolation = cv2.INTER_CUBIC)
					cv2.imshow('Original',res)
					
					print self.user_name+"_"+str(self.video_type)+"_"+str(self.eval_id)+"\\frame"+str(frame_no[ind])+"_original.jpg"
					img1 = cv2.imread(self.user_name+"_"+str(self.video_type)+"_"+str(self.eval_id)+"\\frame"+str(frame_no[ind])+"_original.jpg")
					height, width = img1.shape[:2]
					res1 = cv2.resize(img1,(720/2, 1280/2), interpolation = cv2.INTER_CUBIC)
					cv2.imshow('Test',res1)

					cv2.waitKey(0)
					cv2.destroyAllWindows()

			fig = figure()
			ax1 = fig.add_subplot(111)
			ax1.set_ylabel('score')
			ax1.set_xlabel('frame number')
			col = ax1.plot(frame_no,score_final, 'ro',frame_no,score_final, picker=True)
			#fig.savefig('pscoll.eps')
			fig.canvas.mpl_connect('pick_event', onpick3)

			show()

		#self.start()
		
	def centerWindow(self):
		w = 800
		h = 600
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h - 100)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	def add_text(self,new_text):
		self.analyse_text.set(self.analyse_text.get()+ "\n" + new_text)

	def initUI(self):
		self.parent.title("An Automatic Evaluator for Bharatanatyam (Nritta)")
		self.pack(fill=Tkinter.BOTH, expand=1)

	def done(self):
		self.parent.destroy()
		self.quit