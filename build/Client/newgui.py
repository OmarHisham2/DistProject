


from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog
from tkinter import *
import threading
import tkinter as tk
from PIL import ImageTk, Image
import customtkinter
import queue
from mpi4py import MPI


"""
Some Functions
"""


def openFile():
    TF1.configure(state='normal')
    filepath = filedialog.askopenfilename(title="Select Image",filetypes=(("png images","*.png"),("jpg images","*.jpg"),("jpeg images","*.jpeg")))
    TF1.delete(0,tk.END)
    TF1.insert(0,filepath)
    print(filepath)
    TF1.configure(state='disabled')
    return


ProcessingOptions = ["Gaussian ", "Edge Detection", "Convert To Gray"]


"""The GUI"""

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


root = customtkinter.CTk()

root.title('Kiro\'s Image Processing Application')
root.geometry('700x550')

mode = "dark"


Title_Label = customtkinter.CTkLabel(root,text="Kiro's Image Processing Application",font=("Saira Condensed Bold", 40 * -1 ))
Title_Label.pack(pady=10)


TF1_Label = customtkinter.CTkLabel(root,text="Selected Path",font=("Saira Condensed",25))
TF1_Label.pack(pady=10)

TF1 = customtkinter.CTkEntry(root,width=418,height=62,state='disabled')
TF1.pack(pady=(0,20))

TF2_Label = customtkinter.CTkLabel(root,text="Selected Processing Technique",font=("Saira Condensed",25))
TF2_Label.pack(pady=10)

PT_Choice = customtkinter.CTkOptionMenu(root,width=418,height=62,values=ProcessingOptions,text_color="Black",font=("Saira Condensed Bold", 20 ))
PT_Choice.pack(pady=(0,20))

Upload_Button = customtkinter.CTkButton(root,text='Upload Image',font=("Saira Condensed Bold", 20 ),width=418,height=51,hover_color="#9C1D1D",fg_color="#BD1E1E",corner_radius=10,
                                        command=openFile)
Upload_Button.pack(pady=10)


ApplyTech_Button = customtkinter.CTkButton(root,text='Apply Processing Technique',font=("Saira Condensed Bold", 20 ),width=418,height=51,hover_color="#278917",fg_color="#31A11F",
                                           corner_radius=10,command=printThing)
ApplyTech_Button.pack(pady=10)


root.mainloop()

class WorkerThread(threading.Thread):
 def __init__(self, task_queue):
 threading.Thread.__init__(self)
 self.task_queue = task_queue
 self.comm = MPI.COMM_WORLD
 self.rank = self.comm.Get_rank()


while True:
 task = self.task_queue.get()
 if task is None:
    break
 image, operation = task
 
# Create a queue for tasks
task_queue = queue.Queue()
# Create worker threads
for i in range(MPI.COMM_WORLD.Get_size() - 1):
    WorkerThread(task_queue).start()
