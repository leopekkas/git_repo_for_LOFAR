from Tkinter import TclError
import sys

class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        try:
            self.widget.config(state="normal")
            self.widget.insert('end', text)
            self.widget.config(state="disabled")
            self.widget.see('end')
        except TclError:
            sys.exit()
