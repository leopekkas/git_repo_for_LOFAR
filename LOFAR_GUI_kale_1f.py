from Tkinter import Tk, Menu, StringVar, IntVar, BooleanVar, Checkbutton, Frame, Label, Button, Scrollbar, Text, Toplevel, OptionMenu, E, W, S, N, PhotoImage, Entry
import tkFileDialog as filedialog
import time
import subprocess as sub
from Redirect import *
from File_reader import read_config, print_config, make_predict_file, make_applycal_file, lines_in_wsclean
from File_reader import make_applybeam_file, print_parset, make_sourcedb, print_sourcedb, read_MS_info
from fits_plotting_tool import save_fits, produce_video, icrs_to_helio, plot_single_fits
from UI_helper_functions import disableButtons, enableButtons, setUpCheckbuttons, setUpTerminalLog, setUpInformationLog
from UI_helper_functions import writeToInfoFeed, writeToInfoFeedNoLinebreak, make_info_buttons, proceed_warning_message
import os
import sys

def checkAndRunDropdownInput(variable):
    if (variable.get() == "NDPPP predict.parset"):
        predict_clicked()
    elif (variable.get() == "NDPPP applycal.parset"):
        applycal_clicked()
    elif (variable.get() == "NDPPP applybeam.parset"):
        applybeam_clicked()
    elif (variable.get() == "wsclean"):
        wsclean_clicked()

def predict_clicked():
    disableButtons(buttons)
    predict_btn.update()

    make_predict_file(calibrator_file_name.get(), calibrator_nametag.get(), sourcedb_output.get())

    try:
        # Run NDPPP predict.parset here
        p = sub.call(["NDPPP", "predict.parset"])
        print("NDPPP predict.parset \n")
    except (OSError, KeyboardInterrupt):
        print("Error in running NDPPP predict.parset \n")
        predict_btn.update()
        enableButtons(buttons)

    predict_btn.update()
    enableButtons(buttons)

def applycal_clicked():
    disableButtons(buttons)
    applycal_btn.update()

    make_applycal_file(MS_file_name.get(), calibrator_file_name.get())

    try:
        # Run NDPPP applycal.parset here
        p = sub.call(["NDPPP", "applycal.parset"])
        print("NDPPP applycal.parset \n")
    except (OSError, KeyboardInterrupt):
        print("Error in running NDPPP predict.parsett \n")
        applycal_btn.update()
        enableButtons(buttons)

    applycal_btn.update()
    enableButtons(buttons)

def applybeam_clicked():
    disableButtons(buttons)
    applybeam_btn.update()

    make_applybeam_file(MS_file_name.get())

    try:
        # Run NDPPP applybeam.parset here
        p = sub.call(["NDPPP", "applybeam.parset"])
        print("NDPPP applybeam.parset \n")
    except (OSError, KeyboardInterrupt):
        print("Error in running NDPPP predict.parset \n")
        applybeam_btn.update()
        enableButtons(buttons)

    applybeam_btn.update()
    enableButtons(buttons)

def wsclean_clicked():
    # Run NDPPP predict.parset here
    # Run wsclean here
    try:
        disableButtons(buttons)
        wsclean_btn.update()
        wscommand = read_config(config_file_name.get(), bool_vars, MS_file_name, MS_id, use_datetime, time_format_variable)
        if wscommand==-1:
            print("wsclean exited\n")
        else:
            p = sub.call(wscommand)
            for l in wscommand:
                print(l),
            print("\n")

        wsclean_btn.update()
        enableButtons(buttons)
    except (OSError, KeyboardInterrupt, TypeError):
        print("Error in running the wsclean command \n")
        wsclean_btn.update()
        enableButtons(buttons)

def multiple_plot_clicked():
    filez = filedialog.askopenfilenames(initialdir = os.getcwd(),
                                            title="Select files",
                                            filetypes = ((".fits files", "*.fits"),
                                                        ("all files", "*")))

    lst = list(filez)
    index = 0
    if len(lst) == 0:
        writeToInfoFeed("No file(s) chosen \n", info_text)
    else:
        lst = list(filez)
        index = 0
        for f in lst:
            #f = os.path.basename(f)
            save_fits(f, index)
            index = index + 1
        print("Plotting multiple files \n")

def video_clicked():
    # Call a function that outputs a video from png files
    filez = filedialog.askopenfilenames(initialdir = os.getcwd(),
                                            title="Select files",
                                            filetypes = ((".png files", "*.png"),
                                                        ("all files", "*")))

    try:
        lst = list(filez)
        #for i in range(len(lst)):
        #    lst[i] = os.path.basename(lst[i])
        produce_video(lst)
        print("Saved a video with the name \"video.mp4\" \n")
    except:
        writeToInfoFeed("No file(s) chosen \n", info_text)

def manage_config_clicked():
    config_main_window = Toplevel(root)
    config_main_window.title("Options setup")
    config_main_window.geometry("500x400")
    config_main_window.resizable(False, False)

    top_frame = Frame(config_main_window, width=500, height=100)
    top_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)

    config_window = Frame(config_main_window, width=500, height=300)
    config_window.grid(row=1, column=0, sticky=N+W, padx=5, pady=5)

    config_window_title = Label(top_frame, text="Choose which options you want included in wsclean", font=(main_font, 12, "bold"))
    config_window_title.grid(row=0, column=0, padx=(12, 0), pady=20)

    setUpCheckbuttons(config_window, bool_vars)

def change_fits():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a .fits file for plotting",
                                            filetypes = ((".fits files", "*.fits"),
                                                        ("all files", "*")))

    if not filename:
        writeToInfoFeed("Change the .fits file: No file chosen \n", info_text)
    else:
        fits_file_path.set(filename)

        filename = os.path.basename(filename)

        fits_file_name.set(filename)
        fits_file_name_label.update()

def job_queue_clicked():
    job_queue_window = Toplevel(root)
    job_queue_window.title("Create a job queue")
    job_queue_window.geometry("350x250")
    job_queue_window.resizable(False, False)

    job_queue_frame = Frame(job_queue_window, width=320, height=240, bg=frame_color)
    job_queue_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=N+S+E+W, padx=4, pady=4)
    job_queue_frame.grid_propagate(False)

    job_queue_window.columnconfigure(0, weight=1)
    job_queue_window.rowconfigure(0, weight=1)

    row_ind = 0

    OPTIONS = [
    "None",
    "NDPPP predict.parset",
    "NDPPP applycal.parset",
    "NDPPP applybeam.parset",
    "wsclean"
    ]

    variable1 = StringVar(job_queue_frame)
    variable1.set(OPTIONS[0])

    variable2 = StringVar(job_queue_frame)
    variable2.set(OPTIONS[0])

    variable3 = StringVar(job_queue_frame)
    variable3.set(OPTIONS[0])

    variable4 = StringVar(job_queue_frame)
    variable4.set(OPTIONS[0])

    dropdownmenu1 = OptionMenu(job_queue_frame, variable1, *OPTIONS)
    dropdownmenu1.config(width=23)
    row_ind += 1
    dropdownmenu1.grid(row=row_ind, column=0, padx=(35, 5), pady=(15, 5))

    dropdownmenu2 = OptionMenu(job_queue_frame, variable2, *OPTIONS)
    dropdownmenu2.config(width=23)
    row_ind += 1
    dropdownmenu2.grid(row=row_ind, column=0, padx=(35, 5), pady=5)

    dropdownmenu3 = OptionMenu(job_queue_frame, variable3, *OPTIONS)
    dropdownmenu3.config(width=23)
    row_ind += 1
    dropdownmenu3.grid(row=row_ind, column=0, padx=(35, 5), pady=5)

    dropdownmenu4 = OptionMenu(job_queue_frame, variable4, *OPTIONS)
    dropdownmenu4.config(width=23)
    row_ind += 1
    dropdownmenu4.grid(row=row_ind, column=0, padx=(35, 5), pady=5)

    # Run the job queue
    def queue_clicked():
        waiting_string1.set("Running")
        waiting_label1.update()
        checkAndRunDropdownInput(variable1)
        waiting_string1.set("Done!")
        waiting_label1.update()
        waiting_string2.set("Running")
        waiting_label2.update()
        checkAndRunDropdownInput(variable2)
        waiting_string2.set("Done!")
        waiting_label2.update()
        waiting_string3.set("Running")
        waiting_label3.update()
        checkAndRunDropdownInput(variable3)

        waiting_string3.set("Done!")
        waiting_label3.update()
        waiting_string4.set("Running")
        waiting_label4.update()
        checkAndRunDropdownInput(variable4)
        waiting_string4.set("Done!")
        waiting_label4.update()

    run_queue_btn = Button(job_queue_frame, text="Run the queue", command=queue_clicked)
    row_ind += 1
    run_queue_btn.grid(row=row_ind, column=0, padx=(35, 5), pady=5)

    # Running and waiting texts
    waiting_string1 = StringVar(job_queue_frame)
    waiting_label1 = Label(job_queue_frame, textvariable=waiting_string1, font=(main_font, 11), bg=frame_color)
    waiting_label1.grid(row=1, column=1, sticky = W, padx=5, pady=6)

    waiting_string2 = StringVar(job_queue_frame)
    waiting_label2 = Label(job_queue_frame, textvariable=waiting_string2, font=(main_font, 11), bg=frame_color)
    waiting_label2.grid(row=2, column=1, sticky = W, padx=5, pady=6)

    waiting_string3 = StringVar(job_queue_frame)
    waiting_label3 = Label(job_queue_frame, textvariable=waiting_string3, font=(main_font, 11), bg=frame_color)
    waiting_label3.grid(row=3, column=1, sticky = W, padx=5, pady=6)

    waiting_string4 = StringVar(job_queue_frame)
    waiting_label4 = Label(job_queue_frame, textvariable=waiting_string3, font=(main_font, 11), bg=frame_color)
    waiting_label4.grid(row=4, column=1, sticky = W, padx=5, pady=6)

def donothing():
    x = 0

buttons = []

root = Tk()

# Options included in wsclean
cores = BooleanVar(root, True)
mem = BooleanVar(root, True)
no_reorder = BooleanVar(root, True)
no_update_model_required = BooleanVar(root, True)
mgain = BooleanVar(root, True)
weight_briggs = BooleanVar(root, True)
size = BooleanVar(root, True)
scale = BooleanVar(root, True)
pol = BooleanVar(root, True)
auto_mask = BooleanVar(root, True)
multiscale = BooleanVar(root, True)
auto_threshold = BooleanVar(root, True)
data_column = BooleanVar(root, True)
niter = BooleanVar(root, True)
intervals_out = BooleanVar(root, True)
interval = BooleanVar(root, True)
fit_beam = BooleanVar(root, True)
make_psf = BooleanVar(root, True)

bool_vars = [cores, mem, no_reorder, no_update_model_required, mgain, weight_briggs, size, scale,
                pol, auto_mask, multiscale, auto_threshold, data_column, niter, intervals_out,
                interval, fit_beam, make_psf]

config_file_name = StringVar(root, "config")
config_file_path = StringVar(root, "config")
fits_file_name = StringVar(root, "wsclean-t0000-image.fits")
fits_file_path = StringVar(root, "wsclean-t0000-image.fits")
MS_file_name = StringVar(root, "L242126_SB001_uv.dppp.MS")
MS_id = StringVar(root, "L242126")
MS_subband = StringVar(root, "001")
MS_file_path = StringVar(root, "L242126_SB001_uv.dppp.MS")
calibrator_file_name = StringVar(root, "L242124_SB001_uv.dppp.MS")
calibrator_id = StringVar(root, "L242124")
calibrator_subband = StringVar(root, "001")
calibrator_file_path = StringVar(root, "L242124_SB001_uv.dppp.MS")
calibrator_nametag = StringVar(root, "VirA")
calibrator_name = StringVar(root, "Virgo")
sourcedb_input_path = StringVar(root, "Ateam_LBA_CC.skymodel.txt")
sourcedb_input = StringVar(root, "Ateam_LBA_CC.skymodel.txt")
sourcedb_output = StringVar(root, "Ateam_LBA_CC.sourcedb")

use_datetime = BooleanVar(root, True)
time_format_variable = StringVar(root, "%Y-%m-%d %H:%M:%S")

MS_input_variable = StringVar(root, "ID_SB_uv.dppp.MS")

# Coloring options
main_color = 'white'
frame_color = 'grey'

main_font = "Times"
secondary_font = "Courier"

# Frame geometry
frame_height = 950
frame_width = 1518

# Basic configuration of the main window
root.title("LOFAR GUI 1.0f")
root.config(bg=main_color)
root.geometry('%dx%d' % (frame_width, frame_height))
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

main_row_ind = -1

# The "Left" side of the main window
left_frame = Frame(root, width=920, height=frame_height, bg=frame_color)
left_frame.grid(row=0, column=0, columnspan=1, rowspan=2, sticky=W+S+E+N, padx=(4, 2), pady=4)
left_frame.grid_propagate(False)

lofar_title = Label(left_frame, text="LOFAR GUI", font=(main_font, 28, "bold"), bg=frame_color)
main_row_ind += 1
lofar_title.grid(row=main_row_ind, column=0, sticky=W+N, pady=(60, 45), padx=(50, 5))

# The "Right" side of the main window
right_frame = Frame(root, height=750, background=frame_color)
right_frame.grid(row=0, column=1, columnspan=2, sticky=W+E+S+N, padx=(2, 4), pady=(4, 2))
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(1, weight=1)

# The "Bottom right" frame
right_bottom_frame = Frame(root, height=300, bg=frame_color)
right_bottom_frame.grid(row=1, column=1, columnspan=2, sticky=W+E+S+N, padx=(2, 4), pady=(2, 4))
right_bottom_frame.columnconfigure(0, weight=1)
right_bottom_frame.rowconfigure(1, weight=1)

# The top menu bar of the main window
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=change_fits)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

formatmenu = Menu(menubar, tearoff=0)

MS_input_menu = Menu(menubar, tearoff=0)
MS_input_menu.add_command(label="ID_SB_uv.dppp.MS (default)", command= lambda: MS_input_variable.set("ID_SB_uv.dppp.MS"))
MS_input_menu.add_command(label="ID_SB_uv.MS", command= lambda: MS_input_variable.set("ID_SB_uv.MS"))
MS_input_menu.add_command(label="*.MS", command= lambda: MS_input_variable.set("*.MS"))
MS_input_menu.add_command(label="Free typing", command= lambda: MS_input_variable.set("Free typing"))

formatmenu.add_cascade(label="MS input file format", menu=MS_input_menu)

menubar.add_cascade(label="Format", menu=formatmenu)

settingsmenu = Menu(menubar, tearoff=0)
settingsmenu.add_command(label="Manage the config file", command=manage_config_clicked)
menubar.add_cascade(label="Settings", menu=settingsmenu)

commandmenu = Menu(menubar, tearoff=0)
commandmenu.add_command(label="Job queue", command=job_queue_clicked)
menubar.add_cascade(label="Commands", menu=commandmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# Displaying the files we're working on

main_row_ind+=1
file_info_label = Label(left_frame, text="Files selected:", font=(main_font, 13, "bold"), bg=frame_color)
file_info_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(10, 10), padx=(80, 0))

config_file_label = Label(left_frame, text="Configuration file: ", font=(main_font, 11), bg=frame_color)
config_file_name_label = Label(left_frame, textvariable=config_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
config_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 5))
config_file_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=5, padx=(1, 5))

fits_file_label = Label(left_frame, text=".fits file: ", font=(main_font, 11), bg=frame_color)
fits_file_name_label = Label(left_frame, textvariable=fits_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
fits_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 0))
fits_file_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=5, padx=(1, 5))

# Change/View .MS file

MS_file_label = Label(left_frame, text="Solar MS: ", font=(main_font, 11), bg=frame_color)
MS_file_name_label = Label(left_frame, textvariable=MS_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
MS_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 0))
MS_file_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=5, padx=(1, 5))

# View file contents buttons
def config_contents():
    print_config(config_file_path.get(), info_text)

view_column=2
view_width=6

view_config_btn = Button(left_frame, text="View", command=config_contents, width=view_width)
view_config_btn.grid(row=2, column=view_column, padx=1, pady=(2,5))

def plot_clicked():
    print("Plotted a file called: " + fits_file_name.get() + "\n")
    plot_single_fits(fits_file_path.get())

view_fits_btn = Button(left_frame, text="View", command=plot_clicked, width=view_width)
view_fits_btn.grid(row=3, column=view_column, padx=1, pady=(2,5))

def view_MS_clicked():
    disableButtons(buttons)
    view_MS_btn.update()
    try:
        second_command = "in=" + MS_file_name.get()
        full_command = "msoverview in=" + MS_file_name.get() + " verbose=T"
        output_file = open("msoverview_output.txt", "w")
        p = sub.Popen(["msoverview", second_command, "verbose=T"], stdout=sub.PIPE)
        for line in p.stdout:
            output_file.write(line)
            writeToInfoFeedNoLinebreak(line, info_text)
        writeToInfoFeed("", info_text)
        output_file.close()
        view_MS_btn.update()
        enableButtons(buttons)

    except (OSError, KeyboardInterrupt):
        writeToInfoFeed("Error in reading the .MS-file contents \n", info_text)
        view_MS_btn.update()
        enableButtons(buttons)

view_MS_btn = Button(left_frame, text="View", command=view_MS_clicked, width=view_width)
view_MS_btn.grid(row=4, column=view_column, padx=1, pady=(2,5))

def list_all_MS():
    MS_dict = {}
    try:
        MS_dict = read_MS_info(MS_dict)
    except IOError:
        print("No file called \"MS_info.csv\" found\n")

    writeToInfoFeed("Known MS files:", info_text)

    for key, value in MS_dict.items():
        keyvaluestring = "ID: " + key + "\n  Starting time:   " + value[0] + "\n  Ending time:     " + value[1]
        keyvaluestring += "\n  Images (ntimes): " + value[2] + "\n"
        writeToInfoFeed(keyvaluestring, info_text)

MS_list_btn = Button(left_frame, text="Known MS files", command=list_all_MS, width=11)
MS_list_btn.grid(row=4, column=view_column + 2, padx=(0, 5), pady=(2,5), sticky=W)

buttons.append(view_MS_btn)
buttons.append(MS_list_btn)

# Change config files
def change_config():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a file",
                                            filetypes = (("Text files", "*.txt"),
                                                        ("all files", "*")))

    if not filename:
        writeToInfoFeed("Change the config file: No file chosen \n", info_text)
    else:
        config_file_path.set(filename)

        filename = os.path.basename(filename)

        config_file_name.set(filename)
        config_file_name_label.update()

change_config_btn = Button(left_frame, text="Change", command=change_config)
change_config_btn.grid(row=2, column=view_column+1, padx=1, pady=(2,5))

def set_datetime():
    use_datetime.set(not use_datetime.get())

config_time_checkbox = Checkbutton(left_frame, text = "Use datetime", variable = use_datetime.get(), command=set_datetime)
config_time_checkbox.config(bg = frame_color, highlightthickness=0, bd=0)
config_time_checkbox.grid(row=2, column=view_column+2, padx=(0, 5), pady=(2,5), sticky = W)
config_time_checkbox.select()

change_fits_btn = Button(left_frame, text="Change", command=change_fits)
change_fits_btn.grid(row=3, column=view_column+1, padx=1, pady=(2,5))

change_MS_open = BooleanVar(root, False)

def change_MS(index, MS_input_string):
    if change_MS_open.get() == False:
        change_MS_open.set(True)
        MS_id_entry_feed = Entry(left_frame, text="Solar MS ID", font=(main_font, 11), width=8)
        MS_id_entry_feed.delete(0, 'end')
        MS_id_entry_feed.grid(row=index, column=2, padx=(2, 1), pady=(2,5))
        MS_id_entry_feed.insert(0, "ID:")
        MS_id_entry_feed.config(fg='grey')

        MS_SB_entry_feed = Entry(left_frame, text="Solar MS Subband", font=(main_font, 11), width=7)
        MS_SB_entry_feed.delete(0, 'end')
        MS_SB_entry_feed.grid(row=index, column=3, padx=(0, 4), pady=(2,5))
        MS_SB_entry_feed.insert(0, "Subband:")
        MS_SB_entry_feed.config(fg='grey')

        def handle_focus_in_id(_):
            MS_id_entry_feed.delete(0, 'end')
            MS_id_entry_feed.config(fg='black')

        def handle_focus_in_SB(_):
            MS_SB_entry_feed.delete(0, 'end')
            MS_SB_entry_feed.config(fg='black')

        MS_id_entry_feed.bind("<FocusIn>", handle_focus_in_id)
        MS_SB_entry_feed.bind("<FocusIn>", handle_focus_in_SB)

        if (MS_input_string == "ID_SB_uv.dppp.MS"):
            def handle_enter_MS(txt):
                if (MS_SB_entry_feed.get() == "Subband:" or MS_SB_entry_feed.get() == ""):
                    MS_file_name.set(MS_id_entry_feed.get() + "_SB" + MS_subband.get() + "_uv.dppp.MS")
                else:
                    MS_file_name.set(MS_id_entry_feed.get() + "_SB" + MS_SB_entry_feed.get() + "_uv.dppp.MS")
                    MS_subband.set(MS_SB_entry_feed.get())

                MS_id.set(MS_id_entry_feed.get())
                MS_id_entry_feed.grid_remove()
                MS_SB_entry_feed.grid_remove()
                change_MS_open.set(False)

            MS_id_entry_feed.bind("<Return>", handle_enter_MS)
            MS_SB_entry_feed.bind("<Return>", handle_enter_MS)
        elif (MS_input_string == "ID_SB_uv.MS"):
            def handle_enter_MS(txt):
                if (MS_SB_entry_feed.get() == "Subband:" or MS_SB_entry_feed.get() == ""):
                    MS_file_name.set(MS_id_entry_feed.get() + "_SB" + MS_subband.get() + "_uv.MS")
                else:
                    MS_file_name.set(MS_id_entry_feed.get() + "_SB" + MS_SB_entry_feed.get() + "_uv.MS")
                MS_id.set(MS_id_entry_feed.get())
                MS_subband.set(MS_SB_entry_feed.get())
                MS_id_entry_feed.grid_remove()
                MS_SB_entry_feed.grid_remove()
                change_MS_open.set(False)

            MS_id_entry_feed.bind("<Return>", handle_enter_MS)
            MS_SB_entry_feed.bind("<Return>", handle_enter_MS)

        elif (MS_input_string == "*.MS"):
            MS_SB_entry_feed.grid_remove()
            MS_id_entry_feed.grid_remove()
            MS_id_entry_feed.config(width=16)
            MS_id_entry_feed.grid(row=index, column=2, columnspan=2, padx=(5, 5), pady=(2,5))
            MS_id_entry_feed.delete(0, 'end')
            MS_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_MS(txt):
                MS_file_name.set(MS_id_entry_feed.get() + ".MS")
                MS_id.set(MS_id_entry_feed.get())
                MS_id_entry_feed.grid_remove()
                change_MS_open.set(False)

            MS_id_entry_feed.bind("<Return>", handle_enter_MS)

        else:
            MS_SB_entry_feed.grid_remove()
            MS_id_entry_feed.grid_remove()
            MS_id_entry_feed.config(width=16)
            MS_id_entry_feed.grid(row=index, column=2, columnspan=2, padx=(5, 5), pady=(2,5))
            MS_id_entry_feed.delete(0, 'end')
            MS_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_MS(txt):
                MS_file_name.set(MS_id_entry_feed.get())
                MS_id.set(MS_id_entry_feed.get())
                MS_id_entry_feed.grid_remove()
                change_MS_open.set(False)

            MS_id_entry_feed.bind("<Return>", handle_enter_MS)

    else:
        writeToInfoFeed("Press enter to close the change MS window\n", info_text)

change_MS_btn = Button(left_frame, text="Change", command= lambda: change_MS(5, MS_input_variable.get()))
change_MS_btn.grid(row=4, column=view_column+1, padx=(5, 5), pady=(2,5))

main_row_ind += 1
main_row_ind += 1

queue_title = Label(left_frame, text="Sourcedb entries:", font=(main_font, 13, "bold"), bg=frame_color)
main_row_ind += 1
queue_title.grid(row=main_row_ind, column=0, sticky = W + N, pady=(15, 10), padx=(80, 5))

# Change/View the calibrator .MS file

calibrator_file_label = Label(left_frame, text="Calibrator measurement set: ", font=(main_font, 11), bg=frame_color)
calibrator_file_name_label = Label(left_frame, textvariable=calibrator_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
calibrator_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 0))
calibrator_file_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=5, padx=(1, 5))

def view_calibrator_clicked():
    disableButtons(buttons)
    view_calibrator_btn.update()

    try:
        second_command = "in=" + calibrator_file_name.get()
        full_command = "msoverview in=" + calibrator_file_name.get() + " verbose=T"
        p = sub.Popen(["msoverview", second_command, "verbose=T"], stdout=sub.PIPE)
        for line in p.stdout:
            writeToInfoFeedNoLinebreak(line, info_text)
        writeToInfoFeed("", info_text)
        view_calibrator_btn.update()
        enableButtons(buttons)

    except (OSError, KeyboardInterrupt):
        writeToInfoFeed("Error in reading the .MS-file contents \n", info_text)
        view_calibrator_btn.update()
        enableButtons(buttons)

view_calibrator_btn = Button(left_frame, text="View", command=view_calibrator_clicked, width=view_width)
view_calibrator_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(2,5))
MS_list_btn_2 = Button(left_frame, text="Known MS files", command=list_all_MS, width=11)
MS_list_btn_2.grid(row=main_row_ind, column=view_column + 2, padx=(0, 5), pady=(2,5), sticky=W)

buttons.append(view_calibrator_btn)
buttons.append(MS_list_btn_2)

change_open = BooleanVar(root, False)

def change_calibrator(index, MS_input_string):
    if change_open.get() == False:
        change_open.set(True)
        calibrator_id_entry_feed = Entry(left_frame, text=" Calibrator ID", font=(main_font, 11), width=8)
        calibrator_id_entry_feed.delete(0, 'end')
        calibrator_id_entry_feed.grid(row=index, column=2, padx=(2, 1), pady=(2,5))
        calibrator_id_entry_feed.insert(0, "ID:")
        calibrator_id_entry_feed.config(fg='grey')

        calibrator_SB_entry_feed = Entry(left_frame, text="Calibrator Subband", font=(main_font, 11), width=7)
        calibrator_SB_entry_feed.delete(0, 'end')
        calibrator_SB_entry_feed.grid(row=index, column=3, padx=(0, 4), pady=(2,5))
        calibrator_SB_entry_feed.insert(0, "Subband:")
        calibrator_SB_entry_feed.config(fg='grey')

        def handle_focus_in_calibrator_id(_):
            calibrator_id_entry_feed.delete(0, 'end')
            calibrator_id_entry_feed.config(fg='black')

        def handle_focus_in_calibrator_SB(_):
            calibrator_SB_entry_feed.delete(0, 'end')
            calibrator_SB_entry_feed.config(fg='black')

        calibrator_id_entry_feed.bind("<FocusIn>", handle_focus_in_calibrator_id)

        calibrator_SB_entry_feed.bind("<FocusIn>", handle_focus_in_calibrator_SB)

        if (MS_input_string == "ID_SB_uv.dppp.MS"):
            def handle_enter_calibrator(txt):
                if (calibrator_SB_entry_feed.get() == "Subband:" or calibrator_SB_entry_feed.get() == ""):
                    calibrator_file_name.set(calibrator_id_entry_feed.get() + "_SB" + calibrator_subband.get() + "_uv.dppp.MS")
                else:
                    calibrator_file_name.set(calibrator_id_entry_feed.get() + "_SB" + calibrator_SB_entry_feed.get() + "_uv.dppp.MS")
                    calibrator_subband.set(calibrator_SB_entry_feed.get())
                calibrator_id.set(calibrator_id_entry_feed.get())
                calibrator_id_entry_feed.grid_remove()
                calibrator_SB_entry_feed.grid_remove()
                change_open.set(False)

            calibrator_id_entry_feed.bind("<Return>", handle_enter_calibrator)
            calibrator_SB_entry_feed.bind("<Return>", handle_enter_calibrator)
        elif (MS_input_string == "ID_SB_uv.MS"):
            def handle_enter_calibrator(txt):
                if (calibrator_SB_entry_feed.get() == "Subband:" or calibrator_SB_entry_feed.get() == ""):
                    calibrator_file_name.set(calibrator_id_entry_feed.get() + "_SB" + calibrator_subband.get() + "_uv.MS")
                else:
                    calibrator_file_name.set(calibrator_id_entry_feed.get() + "_SB" + calibrator_SB_entry_feed.get() + "_uv.MS")
                    calibrator_subband.set(calibrator_SB_entry_feed.get())
                calibrator_id.set(calibrator_id_entry_feed.get())
                calibrator_id_entry_feed.grid_remove()
                calibrator_SB_entry_feed.grid_remove()
                change_open.set(False)

            calibrator_id_entry_feed.bind("<Return>", handle_enter_calibrator)
            calibrator_SB_entry_feed.bind("<Return>", handle_enter_calibrator)
        elif (MS_input_string == "*.MS"):
            calibrator_SB_entry_feed.grid_remove()
            calibrator_id_entry_feed.grid_remove()
            calibrator_id_entry_feed.config(width=16)
            calibrator_id_entry_feed.grid(row=index, column=2, columnspan=2, padx=(5, 5), pady=(2,5))
            calibrator_id_entry_feed.delete(0, 'end')
            calibrator_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_calibrator(txt):
                calibrator_file_name.set(calibrator_id_entry_feed.get() + ".MS")
                calibrator_id.set(calibrator_id_entry_feed.get())
                calibrator_id_entry_feed.grid_remove()
                change_open.set(False)

            calibrator_id_entry_feed.bind("<Return>", handle_enter_calibrator)

        else:
            calibrator_SB_entry_feed.grid_remove()
            calibrator_id_entry_feed.grid_remove()
            calibrator_id_entry_feed.config(width=16)
            calibrator_id_entry_feed.grid(row=index, column=2, columnspan=2, padx=(5, 5), pady=(2,5))
            calibrator_id_entry_feed.delete(0, 'end')
            calibrator_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_calibrator(txt):
                calibrator_file_name.set(calibrator_id_entry_feed.get())
                calibrator_id.set(calibrator_id_entry_feed.get())
                calibrator_id_entry_feed.grid_remove()
                change_open.set(False)

            calibrator_id_entry_feed.bind("<Return>", handle_enter_calibrator)

    else:
        writeToInfoFeed("Press enter to close the change window\n", info_text)

change_calibrator_btn = Button(left_frame, text="Change", command= lambda: change_calibrator(9, MS_input_variable.get()))
change_calibrator_btn.grid(row=main_row_ind, column=view_column+1, padx=(5, 5), pady=(2,5))

main_row_ind += 1

calibrator_nametag_label = Label(left_frame, text="Calibrator nametag:", font=(main_font, 11), bg=frame_color)
calibrator_nametag_name_label = Label(left_frame, textvariable=calibrator_nametag, font=(secondary_font, 11), bg=frame_color)
calibrator_nametag_entry = Entry(left_frame, text="VirA", font=(main_font, 11), width=17)
calibrator_nametag_entry.insert(0, "VirA")
calibrator_nametag_entry.config(fg='grey')

main_row_ind+=1
calibrator_nametag_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 5))
calibrator_nametag_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=(5, 7), padx=(1, 5))
calibrator_nametag_entry.grid(row=main_row_ind, column=2, columnspan=2, sticky = W+N, pady=4, padx=(2, 5))

def handle_focus_in_nametag(_):
    calibrator_nametag_entry.delete(0, 'end')
    calibrator_nametag_entry.config(fg='black')

def handle_focus_out_nametag(_):
    calibrator_nametag_entry.delete(0, 'end')
    calibrator_nametag_entry.insert(0, calibrator_nametag.get())
    calibrator_nametag_entry.config(fg='grey')

def handle_enter_nametag(txt):
    calibrator_nametag.set(calibrator_nametag_entry.get())

calibrator_nametag_entry.bind("<FocusIn>", handle_focus_in_nametag)
calibrator_nametag_entry.bind("<FocusOut>", handle_focus_out_nametag)
calibrator_nametag_entry.bind("<Return>", handle_enter_nametag)

def sourcedb_contents():
    print_sourcedb(sourcedb_input_path.get(), info_text)

def change_input_sourcedb():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a file",
                                            filetypes = (("Text files", "*.txt"),
                                                        (".skymodel files", "*.skymodel"),
                                                        ("all files", "*")))

    if not filename:
        writeToInfoFeed("Change the sourcedb file: No file chosen \n", info_text)
    else:
        sourcedb_input_path.set(filename)

        filename = os.path.basename(filename)

        sourcedb_input.set(filename)
        sourcedb_input_name_label.update()

        if proceed_warning_message("", "Should a new sourcedb file be created for this skymodel file?"):
            try:
                make_sourcedb(sourcedb_input.get(), sourcedb_output.get())
            except (OSError, KeyboardInterrupt):
                print("Error in making a new sourcedb, make sure you're inside the LOFAR environment\n")


sourcedb_input_label = Label(left_frame, text="Sourcedb input file: ", font=(main_font, 11), bg=frame_color)
sourcedb_input_name_label = Label(left_frame, textvariable=sourcedb_input, font=(secondary_font, 11), bg=frame_color)
main_row_ind += 1
sourcedb_input_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 5))
sourcedb_input_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=4, padx=(1, 5))

view_sourcedb_btn = Button(left_frame, text="View", command=sourcedb_contents, width=view_width)
view_sourcedb_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(0,5))
change_sourcedb_btn = Button(left_frame, text="Change", command=change_input_sourcedb)
change_sourcedb_btn.grid(row=main_row_ind, column=view_column+1, padx=1, pady=(0,5))

sourcedb_output_label = Label(left_frame, text="Sourcedb output file: ", font=(main_font, 11), bg=frame_color)
sourcedb_output_name_label = Label(left_frame, textvariable=sourcedb_output, font=(secondary_font, 11), bg=frame_color)
main_row_ind += 1
sourcedb_output_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 5))
sourcedb_output_name_label.grid(row=main_row_ind, column=1, sticky = W + N, pady=4, padx=(1, 5))

sourcedb_output_entry = Entry(left_frame, text="Ateam_LBA_CC.sourcedb", font=(main_font, 11), width=17)
sourcedb_output_entry.insert(0, sourcedb_output.get())
sourcedb_output_entry.config(fg='grey')
sourcedb_output_entry.grid(row=main_row_ind, column=2, columnspan=2, sticky = W+N, pady=4, padx=(2, 5))

def handle_focus_in_sourcedb(_):
    sourcedb_output_entry.delete(0, 'end')
    sourcedb_output_entry.insert(0, sourcedb_output.get())
    sourcedb_output_entry.config(fg='black')

def handle_focus_out_sourcedb(_):
    sourcedb_output_entry.delete(0, 'end')
    sourcedb_output_entry.insert(0, sourcedb_output.get())
    sourcedb_output_entry.config(fg='grey')

def handle_enter_sourcedb(txt):
    sourcedb_output.set(sourcedb_output_entry.get())

sourcedb_output_entry.bind("<FocusIn>", handle_focus_in_sourcedb)
sourcedb_output_entry.bind("<FocusOut>", handle_focus_out_sourcedb)
sourcedb_output_entry.bind("<Return>", handle_enter_sourcedb)

col2_row_ind = main_row_ind

commands_btn_width=32

queue_title = Label(left_frame, text="Commands:", font=(main_font, 13, "bold"), bg=frame_color)
main_row_ind += 1
queue_title.grid(row=main_row_ind, column=0, sticky = W + N, pady=(25, 5), padx=(80, 5))

command_btns_index = main_row_ind

make_info_buttons(left_frame, command_btns_index, root)

predict_btn = Button(left_frame, text="NDPPP predict.parset", command=predict_clicked, width=commands_btn_width)
main_row_ind += 1
predict_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 3))
buttons.append(predict_btn)

def view_predict_clicked():
    make_predict_file(calibrator_file_name.get(), calibrator_nametag.get(), sourcedb_output.get())
    if os.path.exists(os.getcwd() + "/predict.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("predict.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the predict.parset contents \n")
    else:
        print("Error, no predict.parset found in the working directory \n")

view_predict_btn = Button(left_frame, text="View", command=view_predict_clicked, width=3)
view_predict_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=(0, 5))
buttons.append(view_predict_btn)

applycal_btn = Button(left_frame, text="NDPPP applycal.parset", command=applycal_clicked, width=commands_btn_width)
main_row_ind += 1
applycal_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 3))
buttons.append(applycal_btn)

def view_applycal_clicked():
    make_applycal_file(MS_file_name.get(), calibrator_file_name.get())
    if os.path.exists(os.getcwd() + "/applycal.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("applycal.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the applycal.parset contents \n")
    else:
        print("Error, no applycal.parset found in the working directory \n")

view_applycal_btn = Button(left_frame, text="View", command=view_applycal_clicked, width=3)
view_applycal_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=(0, 5))
buttons.append(view_applycal_btn)

applybeam_btn = Button(left_frame, text="NDPPP applybeam.parset", command=applybeam_clicked, width=commands_btn_width)
main_row_ind += 1
applybeam_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 3))
buttons.append(applybeam_btn)

def view_applybeam_clicked():
    make_applybeam_file(MS_file_name.get())
    if os.path.exists(os.getcwd() + "/applybeam.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("applybeam.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the applybeam.parset contents \n")
    else:
        print("Error, no applybeam.parset found in the working directory \n")

view_applybeam_btn = Button(left_frame, text="View", command=view_applybeam_clicked, width=3)
view_applybeam_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=(0, 5))
buttons.append(view_applybeam_btn)

wsclean_btn = Button(left_frame, text="wsclean", command=wsclean_clicked, width=commands_btn_width)
main_row_ind += 1
wsclean_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 3))
buttons.append(wsclean_btn)

def view_wsclean_clicked():
    conf_filename = config_file_name.get()
    myvars = {}
    try:
        with open(conf_filename) as f:
            for line in f:
                name, value = line.partition("=")[::2]
                myvars[name.strip()] = str(value)
    except (OSError, IOError, KeyboardInterrupt):
        print("An error occured with reading the config file\n")
        return None

    start_time = "01-01-2000 00:00:00"
    end_time = "01-01-2000 00:00:00"

    if myvars.has_key("start_time"):
        start_time = myvars["start_time"]
    if myvars.has_key("end_time"):
        end_time = myvars["end_time"]
    wscommands = lines_in_wsclean(myvars, bool_vars, MS_file_name, start_time, end_time)
    for x in range(len(wscommands)):
        print(wscommands[x]),

view_wsclean_btn = Button(left_frame, text="View", command=view_wsclean_clicked, width=3)
view_wsclean_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=(0, 5))
buttons.append(view_wsclean_btn)


# Run a coordinate transformation
def coord_clicked():
    filename = fits_file_path.get()

    if not filename:
        writeToInfoFeed("No file chosen for coordinate transformation \n", info_text)
    else:
        icrs_to_helio(filename)

main_row_ind += 1
coord_btn = Button(left_frame, text="Run a coordinate transformation", command=coord_clicked, width=commands_btn_width, state='disabled')
coord_btn.grid(row=main_row_ind, column=0, sticky = W+N, padx=(70, 5), pady=3)

buttons.append(coord_btn)

# Plotting and visualization
visualization_label = Label(left_frame, text="Plotting and visualization:", font=(main_font, 13, "bold"), bg=frame_color)
main_row_ind += 1
visualization_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(20, 5), padx=(80, 5))

plot_many_btn = Button(left_frame, text="Plot & save multiple .fits files", width=25, command=multiple_plot_clicked)
main_row_ind += 1
plot_many_btn.grid(row=main_row_ind, column=0, sticky = N + W, padx=(70, 5), pady=(10, 3))

buttons.append(plot_many_btn)

video_btn = Button(left_frame, text="Wrap multiple plots into a video", width=25, command=video_clicked, state='disabled')
main_row_ind += 1
video_btn.grid(row=main_row_ind, column=0, sticky = N + W, padx=(70, 5), pady=3)

# Text box for an information feed
info_text = setUpInformationLog(right_frame, main_font, frame_color)

# !TODO A function for displaying information on the text widget

# Text log for keeping a track of commands we've already run
setUpTerminalLog(right_bottom_frame, main_font, frame_color)

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
