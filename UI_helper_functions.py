from Tkinter import Tk, Frame, BooleanVar, Checkbutton, Button, W, N, E, S, Menu, Label, Text, Scrollbar, IntVar, Entry, Toplevel
import tkMessageBox
import sys
from Redirect import *

def proceed_warning_message(titletext, text):
    warningboxresult = tkMessageBox.askyesno(title=titletext, message=text)
    return warningboxresult

## Disables a list of buttons
def disableButtons(buttons):
    for b in buttons:
        b.config(state="disabled")

## Changes the state of a list of buttons to normal
def enableButtons(buttons):
    for b in buttons:
        b.config(state="normal")

## Changes a single value inside the configuration file
#
# @param config_file_name Name of the config file
# @param name Name of the value that will be changed
# @param newVal New value for the changed value
def change_config_file_line(config_file_name, name, newVal):
    fileFound = True
    data = []
    # Open the config file and save its contents into a list
    try:
        with open(config_file_name.get()) as f:
            data = f.readlines()
    except (OSError, IOError, KeyboardInterrupt):
        fileFound = False

    if fileFound == False:
        print("No file called " + config_file_name + " found in the cwd\n")
    else:
        foundInd = -1
        for i in range(len(data)):
            data[i] = data[i].strip()
            if (name + "=") in data[i]:
                foundInd = i
            elif (name + " =") in data[i]:
                foundInd = i

        # If we find the entry with a corresponding name, edit it
        # Otherwose make a new entry into the configuration file
        if foundInd != -1:
            data[foundInd] = name + "=" + str(newVal)
        else:
            data.append(name+"="+str(newVal))

        # Write the new contents of the config file back to it
        with open(config_file_name.get(), 'w') as f:
            for line in data:
                f.write(line + "\n")

## Updates a dict of key - value pairs with the contents of a configuration file
#
# @param config_file_name Name of the configuration file
# @param myvars A dictionary that will be updated
#
# @return myvars The dictionary that has been updated
def updateMyvars(config_file_name, myvars):
    data = []
    backupvars = {}
    try:
        with open(config_file_name.get()) as f:
            for line in f:
                name, value = line.partition("=")[::2]
                myvars[name.strip()] = str(value)
    except (OSError, IOError, KeyboardInterrupt):
        return backupvars

    return myvars

## Builds a Tkinter Entry-widget that changes a value inside the configuration file
#
# @param config_window_name A Tkinter Frame-widget
# @param name Name of the value that the Entry widget handles
# @param myvars A dict of key - value pairs for the configuration file
# @param config_file_name Name of the config file
#
# @return A Tkinter Entry-widget
def buildAnEntryBox(config_window, name, myvars, config_file_name):
    font = "Courier"
    name_entry = Entry(config_window, text=name, font=(font, 11), width=10)
    name_entry.config(fg='grey')
    name_entry.insert(0, "No input found")
    if myvars.has_key(name):
        name_entry.delete(0, "end")
        name_entry.insert(0, myvars[name][:-1])

    def handle_focus_in_name_entry(_):
        name_entry.config(fg='black')

    def handle_focus_out_name_entry(_):
        name_entry.config(fg='grey')
        name_entry.delete(0, "end")
        name_entry.insert(0, "No input found")
        if myvars.has_key(name):
            name_entry.delete(0, "end")
            name_entry.insert(0, myvars[name][:-1])

    def handle_enter_name_entry(txt, myvars):
        # Set the file name as
        change_config_file_line(config_file_name, name, name_entry.get())
        myvars = updateMyvars(config_file_name, myvars)
        name_entry.delete(0, "end")
        name_entry.insert(0, myvars[name])
        handle_focus_out_name_entry("dummy")

    name_entry.bind("<FocusIn>", handle_focus_in_name_entry)
    name_entry.bind("<FocusOut>", handle_focus_out_name_entry)
    name_entry.bind("<Return>", lambda x: handle_enter_name_entry("dummy", myvars))

    return name_entry

## Creates an info widget
#
# @param frame Frame in which the button is created
# @param root Main Tkinter window
# @param infotext The information that is shows to the user
#
# @return The information widget
def info_button_factory(frame, root, infotext):
    font = "Times"
    color = "light yellow"

    questionmark_button = Button(frame, text="?", command=None, state='disabled', disabledforeground='black', relief='flat')
    info_window = Toplevel()
    info_window.wm_attributes('-type', 'splash')
    info_window.withdraw()
    info_window.config(bg=color)

    info_label = Label(info_window, text=infotext, font=(font, 10), bg=color, fg='black')
    info_label.pack(expand=True, fill='both', padx=5, pady=(3, 2))

    def on_enter(event):
        info_window.geometry("+%d+%d" % (root.winfo_pointerx() + 10, root.winfo_pointery() - 10))
        info_window.deiconify()

    def on_leave(enter):
        info_window.withdraw()

    questionmark_button.bind("<Enter>", on_enter)
    questionmark_button.bind("<Leave>", on_leave)

    return questionmark_button

## Makes the info buttons for the main window
def make_info_buttons(frame, row_ind, root):
    row_ind+=1
    # Note, the padx/columnspan is a hacky solution but works for now
    predict_parset_info_btn = info_button_factory(frame, root, "Runs NDPPP predict.parset")
    predict_parset_info_btn.grid(row=row_ind, column=3, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    applycal_parset_info_btn = info_button_factory(frame, root, "Applies the calibrator and produces\na CORR_NO_BEAM column into the solar MS")
    applycal_parset_info_btn.grid(row=row_ind, column=3, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    applybeam_parset_info_btn = info_button_factory(frame, root, "Applies the telescope beam(?) into the Solar MS\n and produces a CORRECTED_DATA column into it")
    applybeam_parset_info_btn.grid(row=row_ind, column=3, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    wsclean_info_btn = info_button_factory(frame, root, "Produces .fits files from the MS\naccording to the configuration file")
    wsclean_info_btn.grid(row=row_ind, column=2, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    coordinate_info_btn = info_button_factory(frame, root, "Runs a coordinate transformation")
    coordinate_info_btn.grid(row=row_ind, column=1, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    row_ind+=1
    multiple_plot_info_btn = info_button_factory(frame, root, "Choose multiple .fits files with [ctrl + click] for plotting into png files")
    multiple_plot_info_btn.grid(row=row_ind, column=1, columnspan=2, padx=(2, 0), pady=3, sticky=W+S)

    row_ind+=1
    video_info_btn = info_button_factory(frame, root, "Choose multiple .fits files with [ctrl + click] for plotting into an mp4 file\n (Work in progress)")
    video_info_btn.grid(row=row_ind, column=1, padx=(2, 0), pady=3, sticky=W+S)
