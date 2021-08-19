## @file TextBox.py
# @brief Class structure that builds and manages text fields (information/terminal log)

from Tkinter import Label, Text, Scrollbar, E, W, N, S, Button, Entry
import sys
from Redirect import *

## Initializes a textfield for the user with a scrollbar
class TextBox:
    ## Initializer
    #
    # @param frame Tkinter frame where the textbox is inserted into
    # @param title Title for the TextBox
    # @param height Height in pixels for the text field
    # @param width Width in pixels for the text field
    def __init__(self, frame, title, height, width):
        self.frame = frame
        self.title = title
        self.height = height
        self.width = width
        self.font_size = 9
        self.font_name = "Times"
        self.frame_color = 'grey'
        self.textbox_fg = 'black'
        self.textbox_bg = 'white'
        self.logscrollbar = Scrollbar(frame)

        log_title_label = Label(frame, text=self.title, font=(self.font_name, 13), bg=self.frame_color)
        log_title_label.grid(row=0, column=0, padx=5, pady=(10, 5))
        self.text_log = Text(frame, height=self.height, width=self.width, yscrollcommand=self.logscrollbar.set, state="normal", font=("Courier", self.font_size))
        self.text_log.config(fg = self.textbox_fg, bg = self.textbox_bg)

        self.logscrollbar.grid(row=1, column=1, padx=2, pady=(0, 5), sticky=N+S)
        self.logscrollbar.config(command=self.text_log.yview)

        self.text_log.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky=N+S+E+W)

    def setFontSize(self, newSize):
        self.font_size = newSize

    def setFontName(self, newFont):
        self.font_name = newFont

    def setDarkMode(self):
        self.textbox_fg = 'white'
        self.textbox_bg = 'black'
        self.text_log["fg"] = self.textbox_fg
        self.text_log["bg"] = self.textbox_bg

    def setLightMode(self):
        self.textbox_bg = 'white'
        self.textbox_fg = 'black'
        self.text_log["fg"] = self.textbox_fg
        self.text_log["bg"] = self.textbox_bg

    ## Directs print() functions from the terminal to this screen
    def enableTerminalRedirect(self):
        old_stdout = sys.stdout
        sys.stdout = Redirect(self.text_log)

    ## Adds an entry where the user can highlight text for easy location
    def addHighlightTextEntry(self):
        self.text_log.grid(row=1, column=0, columnspan=4, padx=(5, 0), pady=(0, 5), sticky=N+S+E+W)
        self.logscrollbar.grid(row=1, column=4, padx=2, pady=(0 ,5), sticky=N+S)

        self.search_btn = Button(self.frame, text="Highlight", font=(self.font_name, 11))
        self.search_btn.grid(row=0, column=2, padx=2, pady=(8, 2), sticky=W)

        self.search_entry = Entry(self.frame, text="Find a keyword:", font=(self.font_name, 10))
        self.search_entry.grid(row=0, column=1, padx=5, pady=(8, 2), sticky=E)

        self.search_entry.insert(0, "Find a keyword:")
        self.search_entry.config(fg='grey')

        def find():
            #remove tag 'found' from index 1 to END
            self.text_log.tag_remove('found', '1.0', 'end')

            #returns to widget currently in focus
            s = self.search_entry.get()
            if s:
                idx = '1.0'
                lastidx='end'

                while 1:
                    #searches for desired string from index 1
                    idx = self.text_log.search(s, idx, nocase=1,
                                      stopindex='end')
                    if not idx: break

                    #last index sum of current index and
                    #length of text
                    lastidx = '%s+%dc' % (idx, len(s))

                    #overwrite 'Found' at idx
                    self.text_log.tag_add('found', idx, lastidx)
                    idx = lastidx

                self.text_log.see(lastidx)

                #mark located string as red
                self.text_log.tag_config('found', foreground='red')

        def handle_focus_in(_):
            self.search_entry.delete(0, 'end')
            self.search_entry.config(fg='black')

        def handle_focus_out(_):
            self.search_entry.delete(0, 'end')
            self.search_entry.config(fg='grey')
            self.search_entry.insert(0, 'Find a keyword')

        def handle_enter(txt):
            find()
            handle_focus_out('dummy')
            handle_focus_in('dummy')

        self.search_entry.bind("<FocusIn>", handle_focus_in)
        self.search_entry.bind("<FocusOut>", handle_focus_out)
        self.search_entry.bind("<Return>", handle_enter)

        self.search_btn.config(command= lambda: handle_enter('dummy'))

    ## Tkinter Text.insert()
    def insert(self, index, line):
        self.text_log.insert(index, line)

    ## Tkinter Text.see()
    def see(self, index):
        self.text_log.see(index)

    ## Writes to the Textbox widget, outputs a distinct line after the input line
    #
    # @param line String value which is written into the text widget
    # @param info_text A Tkinter text widget
    def writeToFeed(self, line):
        self.text_log.insert('end', line + "\n")
        self.text_log.insert('end', "\n************************************************************\n\n")
        self.text_log.see('end')

    ## Writes to the Textbox widget without any linebreak at the end
    #
    # @param line String value which is written into the text widget
    # @param info_text A Tkinter text widget
    def writeToFeedNoLinebreak(self, line):
        self.text_log.insert('end', line)
        self.text_log.see('end')
