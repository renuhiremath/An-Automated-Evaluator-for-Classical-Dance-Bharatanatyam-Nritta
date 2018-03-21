import Tkinter
from PIL import Image, ImageTk
import video_to_frames_with_db
import FaceDetection
import UpperBodyDetection
import LowerBodyDetection
import Scoring
import printReportCard

class StartAnalysis(Tkinter.Frame):
	def __init__(self,user_name, video_name,video_type,parent=None):
		Tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.user_name = user_name
		self.video_name = video_name
		self.video_type = video_type
		self.report_card = []
		self.initUI()
		self.centerWindow()
		self.create_labels()
		
	def create_labels(self):
		label1=Tkinter.Label(self,text="Analysing the video...",relief=Tkinter.FLAT)
		label1["padx"]=15
		label1["pady"]=15
		label1["font"]=("comic sans ms",20,"bold underline")
		label1.place(x=200,y=10)
		
		self.analyse_text = Tkinter.StringVar()
		self.analyse_text.set("Starting...")
		label2=Tkinter.Label(self,textvar=self.analyse_text,relief=Tkinter.FLAT)
		label2["padx"]=15
		label2["pady"]=15
		label2["font"]=("comic sans ms",15)
		label2.place(x=150,y=100)

		self.button1=Tkinter.Button(self,text="Start Analysis")
		self.button1["padx"]=30
		self.button1["pady"]=10
		self.button1["relief"]=Tkinter.RIDGE
		self.button1["font"]=("comic sans ms",15)
		self.button1["command"]=self.start
		self.button1.place(x=150,y=450)


		self.button2=Tkinter.Button(self,text="View Results")
		self.button2["padx"]=30
		self.button2["pady"]=10
		self.button2["relief"]=Tkinter.RIDGE
		self.button2["font"]=("comic sans ms",15)
		self.button2["command"]=self.results
		self.button2.place(x=500,y=450)
		
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
		
	def start(self):
		self.add_text("Converting video to frames...")
		self.eval_id = video_to_frames_with_db.convert_video_to_frames(self.user_name,self.video_name,"",self.video_type)
		self.add_text("FaceDetection...")
		results_folder = self.user_name+"_"+str(self.video_type)+"_"+str(self.eval_id)
		FaceDetection.face_detect_main(self.eval_id,results_folder, results_folder)
		self.add_text("UpperBodyDetection...")
		UpperBodyDetection.upperbody_detect_main(self.eval_id,results_folder, results_folder)
		self.add_text("LowerBodyDetection...")
		LowerBodyDetection.lowerbody_detect_main(self.eval_id,results_folder, results_folder)
		self.report_card = Scoring.score(self.user_name,self.video_type)

	def results(self):
		self.parent.destroy()
		root1=Tkinter.Tk()
		chat_window=printReportCard.PrintReportCard(self.user_name,self.report_card, self.eval_id,self.video_type,root1)
		chat_window.mainloop()

if __name__ == "__main__":
	root = Tkinter.Tk()
	chat=StartAnalysis("sam","videos\\samhitha\\correct.mp4",3,root)
	chat.mainloop()