from features.default import BaseFeature
import tkinter as tk


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "open_notepad"
        self.patterns = ["open notepad"]

    def action(self, spoken_text):
        self.notepad()
        return

    '''Notepad for future use maybe'''

    def notepad(self):
        root = tk.Tk()
        root.geometry("300x300")
        root.minsize(height=400, width=350)
        root.maxsize(height=560, width=560)
        root.title("My notepad")

        # implementing scrollbar
        scrollbar = tk.Scrollbar(root)

        # packing the scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # adding typing functionality
        text_info = tk.Text(root, yscrollcommand=scrollbar.set)
        text_info.pack(fill=tk.BOTH)

        # retrieving info from text widget
        def printInput():
            inp = text_info.get(1.0, "end-1c")
            lbl.config(text="Provided Input: "+inp)

        # Button Creation
        printButton = tk.Button(root, text="Done", command=printInput)
        printButton.pack(side=tk.BOTTOM)

        # Label Creation
        lbl = tk.Label(root, text="")
        lbl.pack()

        # configuring the scrollbar
        scrollbar.config(command=text_info.yview)
        root.mainloop()
