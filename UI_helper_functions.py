from Tkinter import Tk, Frame, BooleanVar, Checkbutton, Button, W, N, E, S, Menu, Label, Text, Scrollbar, IntVar, Entry, Toplevel
import tkMessageBox
import sys
from Redirect import *

def proceed_warning_message(titletext, text):
    warningboxresult = tkMessageBox.askyesno(title=titletext, message=text)
    return warningboxresult

def writeToInfoFeed(line, info_text):
    info_text.insert('end', line + "\n")
    info_text.see('end')

def writeToInfoFeedNoLinebreak(line, info_text):
    info_text.insert('end', line)
    info_text.see('end')

def disableButtons(buttons):
    for b in buttons:
        b.config(state="disabled")

def enableButtons(buttons):
    for b in buttons:
        b.config(state="normal")

def setUpCheckbuttons(config_window, bool_vars):
    row_index = 0

    row_index += 1
    cores_cb = Checkbutton(config_window, text="cores", variable=bool_vars[0]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    mem_cb = Checkbutton(config_window, text="memory", variable=bool_vars[1]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    no_reorder_cb = Checkbutton(config_window, text="no-reorder", variable=bool_vars[2]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    no_update_model_required_cb = Checkbutton(config_window, text="no-update-model-required", variable=bool_vars[3]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    mgain_cb = Checkbutton(config_window, text="mgain", variable=bool_vars[4]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    wb_cb = Checkbutton(config_window, text="weight briggs", variable=bool_vars[5]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    size_cb = Checkbutton(config_window, text="size", variable=bool_vars[6]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    scale_cb = Checkbutton(config_window, text="scale", variable=bool_vars[7]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)
    row_index += 1
    pol_cb = Checkbutton(config_window, text="polarisation", variable=bool_vars[8]).grid(row=row_index, column=0, padx=20, pady=5, sticky=W + N)

    row_index = 0

    row_index += 1
    auto_mask_cb = Checkbutton(config_window, text="auto-mask", variable=bool_vars[9]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    multiscale_cb = Checkbutton(config_window, text="multiscale", variable=bool_vars[10]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    auto_threshold_cb = Checkbutton(config_window, text="auto-threshold", variable=bool_vars[11]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    data_column_cb = Checkbutton(config_window, text="data-column", variable=bool_vars[12]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    niter_cb = Checkbutton(config_window, text="niter", variable=bool_vars[13]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    intervals_out_cb = Checkbutton(config_window, text="intervals-out", variable=bool_vars[14]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    interval_start_cb = Checkbutton(config_window, text="interval", variable=bool_vars[15]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    fit_beam_cb = Checkbutton(config_window, text="fit-beam", variable=bool_vars[16]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)
    row_index += 1
    make_psf_cb = Checkbutton(config_window, text="make-psf", variable=bool_vars[17]).grid(row=row_index, column=1, padx=20, pady=5, sticky=W + N)

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

def make_info_buttons(frame, row_ind, root):
    row_ind+=1
    # Note, the padx/columnspan is a hacky solution but works for now
    predict_parset_info_btn = info_button_factory(frame, root, "Runs NDPPP predict.parset")
    predict_parset_info_btn.grid(row=row_ind, column=1, columnspan=2, padx=(57, 0), pady=3, sticky=W+S)

    row_ind+=1
    applycal_parset_info_btn = info_button_factory(frame, root, "Applies the calibrator and produces\na CORR_NO_BEAM column into the solar MS")
    applycal_parset_info_btn.grid(row=row_ind, column=1, columnspan=2, padx=(57, 0), pady=3, sticky=W+S)

    row_ind+=1
    applybeam_parset_info_btn = info_button_factory(frame, root, "Applies the telescope beam(?) into the Solar MS\n and produces a CORRECTED_DATA column into it")
    applybeam_parset_info_btn.grid(row=row_ind, column=1, columnspan=2, padx=(57, 0), pady=3, sticky=W+S)

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
