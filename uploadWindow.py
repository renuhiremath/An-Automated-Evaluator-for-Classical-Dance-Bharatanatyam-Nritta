import Tkinter
from tkFileDialog   import askopenfilename  
from PIL import Image, ImageTk
import re 
import startAnalysis

class UploadWindow(Tkinter.Frame):
	def __init__(self, parent=None):
		Tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		self.centerWindow()
		self.create_labels()
		
	def callback(self):
		name= askopenfilename() 
		if (name != "" and ".mp4" in name ):
			print name
			self.video_name.set(name)
			print "DONE..."
		else:
			print "Invalid file"

	def create_labels(self):
		label1=Tkinter.Label(self,text="Upload a video for analysis...",relief=Tkinter.FLAT)
		label1["padx"]=15
		label1["pady"]=15
		label1["font"]=("comic sans ms",20,"bold underline")
		label1.place(x=200,y=10)
		
		label2=Tkinter.Label(self,text="Username : ",relief=Tkinter.FLAT)
		label2["padx"]=15
		label2["pady"]=15
		label2["font"]=("comic sans ms",15)
		label2.place(x=150,y=100)

		label3=Tkinter.Label(self,text="Video Type (1,2,3,4 or 5) : ",relief=Tkinter.FLAT)
		label3["padx"]=15
		label3["pady"]=15
		label3["font"]=("comic sans ms",15)
		label3.place(x=150,y=200)

		label3=Tkinter.Label(self,text="Video  : ",relief=Tkinter.FLAT)
		label3["padx"]=15
		label3["pady"]=15
		label3["font"]=("comic sans ms",15)
		label3.place(x=150,y=300)

		self.user_name = Tkinter.StringVar()
		e = Tkinter.Entry(self, textvariable=self.user_name)
		e["font"]=("comic sans ms",15)
		e.place(x=450,y=115)

		self.video_type = Tkinter.IntVar()
		e1 = Tkinter.Entry(self, textvariable=self.video_type)
		e1["font"]=("comic sans ms",15)
		e1.place(x=450,y=215)

		self.video_name = Tkinter.StringVar()
		self.e2 = Tkinter.Entry(self, textvariable=self.video_name)
		self.e2["font"]=("comic sans ms",15)
		self.e2.place(x=450,y=315)

		button2=Tkinter.Button(self,text="Upload")
		button2["padx"]=10
		button2["pady"]=5
		button2["relief"]=Tkinter.RIDGE
		button2["font"]=("comic sans ms",10)
		button2["command"]=self.callback
		button2.place(x=710,y=310)

		button1=Tkinter.Button(self,text="Start Analysis")
		button1["padx"]=30
		button1["pady"]=10
		button1["relief"]=Tkinter.RIDGE
		button1["font"]=("comic sans ms",15)
		button1["command"]=self.start_analysis
		button1.place(x=300,y=450)
		
	def centerWindow(self):
		w = 800
		h = 600
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h - 100)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	def initUI(self):
		self.parent.title("An Automatic Evaluator for Bharatanatyam (Nritta)")
		self.pack(fill=Tkinter.BOTH, expand=1)
		
	def start_analysis(self):
		if (self.user_name.get() == ""):
			print "Enter a username"
		elif (not self.video_type.get() in [1,2,3,4,5]):
			print "Enter the valid video type"
		elif (self.video_name.get() == ""):
			print "Upload a video"
		else:
			self.parent.destroy()
			root1=Tkinter.Tk()
			chat_window=startAnalysis.StartAnalysis(self.user_name.get(),self.video_name.get(),self.video_type.get(), root1)
			chat_window.mainloop()

if __name__ == "__main__":
	root = Tkinter.Tk()
	chat = UploadWindow(root)
	chat.mainloop()