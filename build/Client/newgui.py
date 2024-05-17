


from pathlib import Path
import uuid
import boto3
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog
from tkinter import *
import threading
import tkinter as tk
from PIL import ImageTk, Image
import customtkinter
import queue
import cv2
from mpi4py import MPI


"""
Some Functions
"""
s3 = boto3.resource('s3')

filepath = None


def openFile():
    global filepath
    TF1.configure(state='normal')
    filepath = filedialog.askopenfilename(title="Select Image",filetypes=(("png images","*.png"),("jpg images","*.jpg"),("jpeg images","*.jpeg")))
    TF1.delete(0,tk.END)
    TF1.insert(0,filepath)
    TF1.configure(state='disabled')
    return

def uploadFile():
    chosenTechnique = selectedTechnique.get()
    uniqueID = str(uuid.uuid4())
    with open(uniqueID+'.txt',"w") as file:
        file.write(chosenTechnique)
    if(filepath is not None):
        s3.meta.client.upload_file(filepath,'bucket441122',uniqueID+'.png')
        s3.meta.client.upload_file(uniqueID+'.txt','bucket441122',uniqueID+'.txt')
        print('File uploaded successfully :) ')
    else:
        print('image failed to upload!')
    return

ProcessingOptions = ["Gaussian", "Edge Detection", "Convert To Gray"]


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


selectedTechnique = StringVar(TF2_Label) 
selectedTechnique.set(ProcessingOptions[0])

PT_Choice = customtkinter.CTkOptionMenu(root,width=418,height=62,values=ProcessingOptions,text_color="Black",font=("Saira Condensed Bold", 20 ),
                                        variable=selectedTechnique)
PT_Choice.pack(pady=(0,20))



Upload_Button = customtkinter.CTkButton(root,text='Upload Image',font=("Saira Condensed Bold", 20 ),width=418,height=51,hover_color="#9C1D1D",fg_color="#BD1E1E",corner_radius=10,
                                        command=openFile)
Upload_Button.pack(pady=10)


ApplyTech_Button = customtkinter.CTkButton(root,text='Apply Processing Technique',font=("Saira Condensed Bold", 20 ),width=418,height=51,hover_color="#278917",fg_color="#31A11F",
                                           corner_radius=10,command=uploadFile)
ApplyTech_Button.pack(pady=10)


root.mainloop()


