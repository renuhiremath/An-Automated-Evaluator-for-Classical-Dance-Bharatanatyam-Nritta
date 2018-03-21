import Tkinter
from PIL import Image, ImageTk
import uploadWindow

class App(Tkinter.Frame):
	def __init__(self, parent=None):
		Tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		self.centerWindow()
		self.create_labels()
		
	def create_labels(self):
		x1=self.parent.winfo_screenwidth()/2-500
		app_name = Tkinter.StringVar()
		app_name.set(""" An Automatic Evaluator\nfor Bharatanatyam (Nritta)""")
		label1=Tkinter.Label(self,textvar=app_name,relief=Tkinter.FLAT)
		label1["padx"]=15
		label1["pady"]=15
		label1["font"]=("comic sans ms",20,"bold underline")
		label1.place(x=x1,y=10)
		
		intro_text=Tkinter.StringVar()
		intro_text.set(""" This is an application that helps score a bharatnatyam\nperformance based on a choreographer's video.\n\n""")
		intro=Tkinter.Label(self,textvar=intro_text)
		intro["padx"]=30
		intro["pady"]=10
		intro["font"]=("comic sans ms",15)
		intro.place(x=100,y=120)
		"""
		i = ImageTk.PhotoImage(Image.open("analysis.jpg"))
		img  = Tkinter.Label(self,image=i, width = 200, height = 200)
		img.place(x=120,y=170)
		"""
		button1=Tkinter.Button(self,text="Upload new Video")
		button1["padx"]=30
		button1["pady"]=10
		button1["relief"]=Tkinter.RIDGE
		button1["font"]=("comic sans ms",15)
		button1["command"]=self.upload_new_video
		button1.place(x=150,y=450)

		button2=Tkinter.Button(self,text="View Analysis")
		button2["padx"]=30
		button2["pady"]=10
		button2["relief"]=Tkinter.RIDGE
		button2["font"]=("comic sans ms",15)
		button2["command"]=self.view_analysis
		#button2.place(x=450,y=450)
		
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
		
	def view_analysis(self):
		self.parent.destroy()
		root1=Tkinter.Tk()
		chat_window=startChatWindow.StartChatWindow(root1)
		chat_window.mainloop()
		
	def upload_new_video(self):
		self.parent.destroy()
		root1=Tkinter.Tk()
		chat_window=uploadWindow.UploadWindow(root1)
		chat_window.mainloop()

root = Tkinter.Tk()
chat=App(root)
chat.mainloop()