from Tkinter import Tk, Frame, BooleanVar, Checkbutton, Button, W, N, E, S, Menu, Label, Text, Scrollbar, IntVar, Entry, Toplevel
import tkMessageBox
import sys
from Redirect import *

def proceed_warning_message(titletext, text):
    warningboxresult = tkMessageBox.askyesno(title=titletext, message=text)
    return warningboxresult

## Writes to a Tkinter Text widget, outputs a distinct line after the input line
#
# @param line String value which is written into the text widget
# @param info_text A Tkinter text widget
def writeToInfoFeed(line, info_text):
    info_text.insert('end', line + "\n")
    info_text.insert('end', "\n************************************************************\n\n")
    info_text.see('end')

## Writes to a Tkinter Text widget without a line break
#
# @param line String value which is written into the text widget
# @param info_text A Tkinter text widget
def writeToInfoFeedNoLinebreak(line, info_text):
    info_text.insert('end', line)
    info_text.see('end')

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

## Sets up checkbuttons for a Manage config window (Move to its own class)
def setUpCheckbuttons(config_window, bool_vars, config_file_name):
    myvars = {}
    FileFound = True

    try:
        with open(config_file_name.get()) as f:
            for line in f:
                name, value = line.partition("=")[::2]
                myvars[name.strip()] = str(value)
    except (OSError, IOError, KeyboardInterrupt):
        FileFound = False

    row_index = 0

    row_index += 1
    cores_cb = Checkbutton(config_window, text="cores", variable=bool_vars[0]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    cores_entry = buildAnEntryBox(config_window, "cores", myvars, config_file_name)
    cores_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    mem_cb = Checkbutton(config_window, text="memory", variable=bool_vars[1]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    mem_entry = buildAnEntryBox(config_window, "memory_limit", myvars, config_file_name)
    mem_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    no_reorder_cb = Checkbutton(config_window, text="no-reorder", variable=bool_vars[2]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    row_index += 1
    no_update_model_required_cb = Checkbutton(config_window, text="no-update-model-required", variable=bool_vars[3]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    row_index += 1
    mgain_cb = Checkbutton(config_window, text="mgain", variable=bool_vars[4]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    mgain_entry = buildAnEntryBox(config_window, "mgain", myvars, config_file_name)
    mgain_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    wb_cb = Checkbutton(config_window, text="weight briggs", variable=bool_vars[5]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    wb_entry = buildAnEntryBox(config_window, "weight_briggs", myvars, config_file_name)
    wb_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    size_cb = Checkbutton(config_window, text="size", variable=bool_vars[6]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    size1_entry = buildAnEntryBox(config_window, "size", myvars, config_file_name)
    size1_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)
    row_index += 1
    size2_label = Label(config_window, text="size (y):").grid(row=row_index, column=0, padx=(10, 2), pady=5, sticky=W)
    size2_entry = buildAnEntryBox(config_window, "size2", myvars, config_file_name)
    size2_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    scale_cb = Checkbutton(config_window, text="scale", variable=bool_vars[7]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    scale_entry = buildAnEntryBox(config_window, "scale", myvars, config_file_name)
    scale_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    pol_cb = Checkbutton(config_window, text="polarisation", variable=bool_vars[8]).grid(row=row_index, column=0, padx=2, pady=5, sticky=W + N)
    pol_entry = buildAnEntryBox(config_window, "polarisation", myvars, config_file_name)
    pol_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index = 0

    row_index += 1
    auto_mask_cb = Checkbutton(config_window, text="auto-mask", variable=bool_vars[9]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    automask_entry = buildAnEntryBox(config_window, "auto_mask", myvars, config_file_name)
    automask_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    multiscale_cb = Checkbutton(config_window, text="multiscale", variable=bool_vars[10]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)

    row_index += 1
    auto_threshold_cb = Checkbutton(config_window, text="auto-threshold", variable=bool_vars[11]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    threshold_entry = buildAnEntryBox(config_window, "auto_threshold", myvars, config_file_name)
    threshold_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    data_column_cb = Checkbutton(config_window, text="data-column", variable=bool_vars[12]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    data_entry = buildAnEntryBox(config_window, "data_column", myvars, config_file_name)
    data_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    niter_cb = Checkbutton(config_window, text="niter", variable=bool_vars[13]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    niter_entry = buildAnEntryBox(config_window, "n_iter", myvars, config_file_name)
    niter_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    intervals_out_cb = Checkbutton(config_window, text="intervals-out", variable=bool_vars[14]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    intervals_out_entry = buildAnEntryBox(config_window, "intervals_out", myvars, config_file_name)
    intervals_out_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    interval_start_cb = Checkbutton(config_window, text="interval", variable=bool_vars[15]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)
    start_entry = buildAnEntryBox(config_window, "start_time", myvars, config_file_name)
    start_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)
    row_index += 1
    interval_end_time = Label(config_window, text="Interval end:").grid(row=row_index, column=3, padx=(10, 2), pady=5, sticky=W)
    end_entry = buildAnEntryBox(config_window, "end_time", myvars, config_file_name)
    end_entry.grid(row=row_index, column=4, padx=(0, 10), sticky=W)

    row_index += 1
    fit_beam_cb = Checkbutton(config_window, text="fit-beam", variable=bool_vars[16]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)

    row_index += 1
    make_psf_cb = Checkbutton(config_window, text="make-psf", variable=bool_vars[17]).grid(row=row_index, column=3, padx=2, pady=5, sticky=W + N)

## Terminal log (Make its own class)
def setUpTerminalLog(right_bottom_frame, main_font, frame_color):
    font_size = 9

    log_title_label = Label(right_bottom_frame, text="Terminal log", font=(main_font, 13), bg=frame_color)

    log_title_label.grid(row=0, column=0, padx=5, pady=(10, 5))

    logscrollbar = Scrollbar(right_bottom_frame)
    logscrollbar.grid(row=1, column=1, padx=2, pady=(0, 5), sticky=N+S)

    text_log = Text(right_bottom_frame, height=18, width=55, yscrollcommand=logscrollbar.set, state="normal", font=("Courier", font_size))
    logscrollbar.config(command=text_log.yview)
    text_log.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky=N+S+E+W)
    old_stdout = sys.stdout
    sys.stdout = Redirect(text_log)

## Information log (Make its own class)
def setUpInformationLog(right_frame, main_font, frame_color):
    font_size = 9

    info_title_label = Label(right_frame, text="Information feed", font=(main_font, 13), bg=frame_color)
    info_title_label.grid(row=0, column=0, padx=5, pady=(10, 0))

    search_entry = Entry(right_frame, text="Find a keyword:", font=(main_font, 10))
    search_entry.grid(row=0, column=1, padx=5, pady=(8, 2), sticky=E)

    search_entry.insert(0, "Find a keyword:")
    search_entry.config(fg='grey')

    search_btn = Button(right_frame, text="Highlight", font=(main_font, 11))
    search_btn.grid(row=0, column=2, padx=2, pady=(8, 2), sticky=W)

    yscrollbar = Scrollbar(right_frame)
    yscrollbar.grid(row=1, column=4, padx=2, pady=5, sticky=N+S)

    info_text = Text(right_frame, height=30, width=65, yscrollcommand=yscrollbar.set, state="normal", font=("Courier", font_size))
    yscrollbar.config(command=info_text.yview)
    info_text.grid(row=1, column=0, columnspan=4, padx=(5, 0), pady=5, sticky=N+S+E+W)

    def find():
        #remove tag 'found' from index 1 to END
        info_text.tag_remove('found', '1.0', 'end')

        #returns to widget currently in focus
        s = search_entry.get()
        if s:
            idx = '1.0'
            lastidx='end'

            while 1:
                #searches for desired string from index 1
                idx = info_text.search(s, idx, nocase=1,
                                  stopindex='end')
                if not idx: break

                #last index sum of current index and
                #length of text
                lastidx = '%s+%dc' % (idx, len(s))

                #overwrite 'Found' at idx
                info_text.tag_add('found', idx, lastidx)
                idx = lastidx

            info_text.see(lastidx)

            #mark located string as red
            info_text.tag_config('found', foreground='red')

    def handle_focus_in(_):
        search_entry.delete(0, 'end')
        search_entry.config(fg='black')

    def handle_focus_out(_):
        search_entry.delete(0, 'end')
        search_entry.config(fg='grey')
        search_entry.insert(0, 'Find a keyword')

    def handle_enter(txt):
        find()
        handle_focus_out('dummy')
        handle_focus_in('dummy')

    search_entry.bind("<FocusIn>", handle_focus_in)
    search_entry.bind("<FocusOut>", handle_focus_out)
    search_entry.bind("<Return>", handle_enter)

    search_btn.config(command= lambda: handle_enter('dummy'))

    return info_text

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
    #wsclean_info_btn.grid(row=row_ind, column=1, columnspan=2, padx=(57, 0), pady=3, sticky=W+S)

    row_ind+=1
    coordinate_info_btn = info_button_factory(frame, root, "Runs a coordinate transformation")
    #coordinate_info_btn.grid(row=row_ind, column=1, padx=0, pady=3, sticky=W+S)

    row_ind+=1
    row_ind+=1
    multiple_plot_info_btn = info_button_factory(frame, root, "Choose multiple .fits files with [ctrl + click] for plotting into png files")
    #multiple_plot_info_btn.grid(row=row_ind, column=0, columnspan=2, padx=(303, 0), pady=(10, 3), sticky=W+S)

    row_ind+=1
    video_info_btn = info_button_factory(frame, root, "Choose multiple .fits files with [ctrl + click] for plotting into an mp4 file\n (Work in progress)")
    #video_info_btn.grid(row=row_ind, column=0, columnspan=2, padx=(303, 0), pady=3, sticky=W+S)

## A factory function that returns an Entry that can change the values for .parset options
#
# @param frame Tkinter Frame
# @param name A unique name for this entry
# @param value The "StringVar" value that is changed via the Entry
#
# @return A Tkinter Entry widget
def make_parset_entry(frame, name, value):
    font = "Times"
    name_entry = Entry(frame, text = name, font=(font, 11), width=13)
    name_entry.config(fg='grey')
    name_entry.delete(0, "end")
    name_entry.insert(0, value.get())

    def handle_focus_in_name_entry(_):
        name_entry.config(fg='black')

    def handle_focus_out_name_entry(_):
        name_entry.config(fg='grey')
        name_entry.delete(0,"end")
        name_entry.insert(0, value.get())

    def handle_enter_name_entry(txt):
        value.set(name_entry.get())
        name_entry.delete(0, "end")
        handle_focus_out_name_entry("dummy")

    name_entry.bind("<FocusIn>", handle_focus_in_name_entry)
    name_entry.bind("<FocusOut>", handle_focus_out_name_entry)
    name_entry.bind("<Return>", handle_enter_name_entry)

    return name_entry

## Sets up the manage predict window (move to its own class)
def setUpPredictEntries(frame, msout, solint, calibrator, sourcedb, caltype, usebeammodel, onebeamperpatch):
    row_index = 0
    row_index += 1
    msout_label = Label(frame, text="msout: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    msout_entry = make_parset_entry(frame, "msout", msout)
    msout_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    solint_label = Label(frame, text="Solution interval: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    solint_entry = make_parset_entry(frame, "solint", solint)
    solint_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    cal_label = Label(frame, text="Calibrator: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    cal_entry = make_parset_entry(frame, "calibrator", calibrator)
    cal_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    sourcedb_label = Label(frame, text="Sourcedb: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    sourcedb_entry = make_parset_entry(frame, "sourcedb", sourcedb)
    sourcedb_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    caltype_label = Label(frame, text="caltype: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    caltype_entry = make_parset_entry(frame, "caltype", caltype)
    caltype_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

## Sets up the manage applycal window (move to its own class)
def setUpApplycalEntries(frame, msout, datacolumn_in, datacolumn_out, parmdb, updateweights):
    row_index = 0
    row_index += 1
    msout_label = Label(frame, text="msout: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    msout_entry = make_parset_entry(frame, "msout", msout)
    msout_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    datacolumn_in_label = Label(frame, text="Datacolumn (in): ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    datacolumn_in_entry = make_parset_entry(frame, "datacolumn_in", datacolumn_in)
    datacolumn_in_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    datacolumn_out_label = Label(frame, text="Datacolumn (out): ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    datacolumn_out_entry = make_parset_entry(frame, "datacolumn_out", datacolumn_out)
    datacolumn_out_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    parmdb_label = Label(frame, text="Parmdb: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    parmdb_entry = make_parset_entry(frame, "parmdb", parmdb)
    parmdb_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

## Sets up the manage applybeam window (move to its own class)
def setUpApplybeamEntries(frame, msout, datacolumn_in, datacolumn_out, updateweights):
    row_index = 0
    row_index += 1
    msout_label = Label(frame, text="msout: ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    msout_entry = make_parset_entry(frame, "msout", msout)
    msout_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    datacolumn_in_label = Label(frame, text="Datacolumn (in): ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    datacolumn_in_entry = make_parset_entry(frame, "datacolumn_in", datacolumn_in)
    datacolumn_in_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)

    row_index += 1
    datacolumn_out_label = Label(frame, text="Datacolumn (out): ", font=("Times", 11)).grid(row=row_index, column=0, padx=5, pady=5, sticky=W)
    datacolumn_out_entry = make_parset_entry(frame, "datacolumn_out", datacolumn_out)
    datacolumn_out_entry.grid(row=row_index, column=1, padx=(0, 10), sticky=W)
