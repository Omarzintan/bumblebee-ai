from tkinter import *
from threading import Thread

global dialogue_root
global dialogue_text_box

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

'''
Deprecated. This will not be useful for bumblebee.
Notepad for the Bumblebee's dialogue box (face).
This opens up the dialogue box/face of Bumblebee.
'''
def start_dialogue():
    
    global dialogue_root
    global dialogue_text_box
    
    dialogue_root = Tk()
    dialogue_root.geometry("300x70")
    dialogue_root.title("Bumblebee")

    scrollbar = Scrollbar(dialogue_root)
    scrollbar.pack(side = RIGHT, fill = Y)

    dialogue_text_box = Text(dialogue_root, yscrollcommand=scrollbar.set)
    dialogue_text_box.pack(fill = BOTH)

    scrollbar.config(command = dialogue_text_box.yview)
    #dialogue_root.mainloop()

    return dialogue_root


'''
Enter dialogue into Bumblebee's dialogue box.
'''
def enter_dialogue(text_box, text):
    global dialogue_text_box

    dialogue_text_box.insert(END, text)

'''
Close Bumblebee's dialogue box.
'''    
def close_dialogue(root):
    print('Dialogue Closed')
    dialogue_root.destroy()



