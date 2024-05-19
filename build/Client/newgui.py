


from pathlib import Path
import time
import uuid
import boto3
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog
from tkinter import *
import threading
import tkinter as tk
from tkinter import ttk
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
    my_progressbar.step()
    chosenTechnique = selectedTechnique.get()
    uniqueID = str(uuid.uuid4())
    with open(uniqueID+'.txt',"w") as file:
        file.write(chosenTechnique)
        my_progressbar.step()

    if(filepath is not None):
        my_progressbar.step()
        s3.meta.client.upload_file(uniqueID+'.txt','bucket441122',uniqueID+'.txt')
        print('Process Sent')
        my_progressbar.step()

        time.sleep(2)
        s3.meta.client.upload_file(filepath,'bucket441122',uniqueID+'.png')
        my_progressbar.step()

        print('Image Sent')
        resultNotFound = True
        my_progressbar.step()
        while(resultNotFound):
            s3Client = boto3.client('s3')
            response = s3Client.list_objects_v2(Bucket="bucket441122")
            for content in response.get('Contents', []):
                if (content['Key'] == "fixed/"+ uniqueID+'_fixed.png'):
                    print('Fix Found!')
                    s3Client.download_file("bucket441122","fixed/"+uniqueID+'_fixed.png',uniqueID+'.png')
                    img = cv2.imread(uniqueID+".png")
                    cv2.imshow('Result',img)
                    cv2.waitKey()
                    resultNotFound = False
                    my_progressbar.step()
                    break
        my_progressbar.step()
    else:
        tk.messagebox.showinfo(title='Error!', message='Select An Image to apply the technique!')
        print('image failed to upload!')
    return

ProcessingOptions = ["edgeDetection","colorInversion","convertToGray","applyBlurring","applyGaussianBlur",
                     "removeNoise","increaseBrightness","resizeToHalf","applyDilation","applyErosion"]


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

my_progressbar =  customtkinter.CTkProgressBar(master=root,progress_color='green')
my_progressbar.pack(pady=20)
my_progressbar.set(0)

root.mainloop()


