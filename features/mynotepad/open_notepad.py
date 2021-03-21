from features.features import BaseFeature
from features.global_vars import bumble_speech as bs
from features.mynotepad import helpers
from tkinter import *

class OpenNotepad(BaseFeature):
    def __init__(self, keywords):
        self.keywords = keywords

    def action(self, spoken_text):
        self.notepad()
        return

    '''Notepad for future use maybe'''
    def notepad():
        root = Tk()
        root.geometry("300x300")
        root.minsize(height=400, width=350)
        root.maxsize(height=560, width=560)
        root.title("My notepad")

        # implementing scrollbar
        scrollbar = Scrollbar(root)

        # packing the scrollbar
        scrollbar.pack(side = RIGHT, fill = Y)

        # adding typing functionality
        text_info = Text(root, yscrollcommand=scrollbar.set)
        text_info.pack(fill = BOTH)


        # retrieving info from text widget
        def printInput():
            inp = text_info.get(1.0, "end-1c")
            lbl.config(text = "Provided Input: "+inp)

        # Button Creation
        printButton = Button(root, text = "Done", command = printInput)
        printButton.pack(side = BOTTOM)

        # Label Creation
        lbl = Label(root, text = "")
        lbl.pack()
    
        # configuring the scrollbar
        scrollbar.config(command = text_info.yview)
        root.mainloop()
