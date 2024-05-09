


from pathlib import Path


from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog
from tkinter import *

import tkinter as tk
from PIL import ImageTk, Image
import customtkinter


"""
Some Functions
"""


def openFile():
    entry_1.configure(state='normal')
    filepath = filedialog.askopenfilename(title="Select Image",filetypes=(("png images","*.png"),("jpg images","*.jpg"),("jpeg images","*.jpeg")))
    entry_1.delete(0,tk.END)
    entry_1.insert(0,filepath)
    print(filepath)
    entry_1.configure(state='disabled')
    return

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


ProcessingOptions = ["Gaussian ", "Edge Detection", "Convert To Gray"]


"""The GUI"""

        
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Downloads\DistProject\build\Client\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1137x683")
window.configure(bg = "#FFFFFF")



canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 683,
    width = 1137,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1137.0,
    130.0,
    fill="#16255B",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=openFile,
    relief="flat"
)
button_1.place(
    x=47.0,
    y=475.0,
    width=418.0,
    height=51.0
)



button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=45.0,
    y=539.0,
    width=418.0,
    height=51.0
)

canvas.create_text(
    254.0,
    39.0,
    anchor="nw",
    text="Kiro’s Image Processing Application",
    fill="#FFFFFF",
    font=("SairaCondensed Bold", 40 * -1)
)

canvas.create_text(
    45.0,
    148.0,
    anchor="nw",
    text="Add Image",
    fill="#16255B",
    font=("SairaCondensed Bold", 50 * -1)
)

canvas.create_text(
    45.0,
    225.0,
    anchor="nw",
    text="Selected Path",
    fill="#727c9c",
    font=("SairaCondensed Bold", 32 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    254.0,
    306.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#BDB2B2",
    fg="#000716",
    disabledbackground="#BDB2B2",
    disabledforeground="#000716",
    highlightthickness=0,
    state='disabled',font=("SairaCondensed", 15 * -1,)
)
entry_1.place(
    x=55.0,
    y=275.0,
    width=398.0,
    height=60.0
)

canvas.create_text(
    45.0,
    350.0,
    anchor="nw",
    text="Selected Processing Technique",
    fill="#727C9C",
    font=("SairaCondensed Bold", 32 * -1)
)

chosenTechnique = StringVar()
chosenTechnique.set('Select A Processing Technique!')

processing_selection = customtkinter.CTkOptionMenu(window,values=ProcessingOptions,width=418,height=62,bg_color='#BDB2B2',fg_color='#000716')
processing_selection.place(
    x=45.0,
    y=404.0
)


# entry_image_2 = PhotoImage(
#     file=relative_to_assets("entry_2.png"))
# entry_bg_2 = canvas.create_image(
#     256.0,
#     434.5,
#     image=entry_image_2
# )
# entry_2 = Entry(
#     bd=0,
#     bg="#BDB2B2",
#     fg="#000716",
#     highlightthickness=0
# )
# entry_2.place(
#     x=57.0,
#     y=404.0,
#     width=398.0,
#     height=59.0
# )




canvas

canvas.create_rectangle(
    667.0,
    214.0,
    1096.0,
    558.0,
    fill="",
    outline="black",
   )



canvas.create_text(
    827.0,
    568.0,
    anchor="nw",
    text="Selected Image",
    fill="#000000",
    font=("SairaCondensed Regular", 20 * -1)
)

window.resizable(False, False)
window.mainloop()
