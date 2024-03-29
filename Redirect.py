## @file Redirect.py
# @brief Redirects text information from the terminal to a Tkinter widget

from Tkinter import TclError
import sys

## Redirects text information from the terminal to a Tkinter widget
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
