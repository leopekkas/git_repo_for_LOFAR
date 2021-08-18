from Tkinter import Tk, Menu, StringVar, IntVar, BooleanVar, Checkbutton, Frame, Label, Button, Scrollbar, Text, Toplevel, OptionMenu, E, W, S, N, PhotoImage, Entry
import tkFileDialog as filedialog
import time
import subprocess as sub
from Redirect import *
from File_reader import read_config, make_predict_file, make_applycal_file, lines_in_wsclean
from File_reader import make_applybeam_file, print_parset, make_sourcedb
from fits_plotting_tool import save_fits, produce_video, icrs_to_helio, plot_single_fits
from UI_helper_functions_py2 import disableButtons, enableButtons
from UI_helper_functions_py2 import make_info_buttons, proceed_warning_message
from TextBox import TextBox
from ButtonFunctions import load_clicked, save_clicked, predict_clicked, applycal_clicked, applybeam_clicked
from ButtonFunctions import wsclean_clicked, darklightmodeswitch, view_calibrator_clicked, view_MS_clicked
from ButtonFunctions import skymodel_contents, view_predict_clicked, view_applycal_clicked, view_applybeam_clicked
from ButtonFunctions import print_config, view_wsclean_clicked
from SettingWindows import manage_predict_clicked, manage_applycal_clicked, manage_applybeam_clicked
from SettingWindows import manage_config_clicked
import os

def change_fits():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a .fits file for plotting",
                                            filetypes = ((".fits files", "*.fits"),
                                                        ("all files", "*")))

    if not filename:
        info_text.writeToFeed("Change the .fits file: No file chosen \n")
    else:
        fits_file_path.set(filename)

        filename = os.path.basename(filename)

        fits_file_name.set(filename)
        fits_file_name_label.update()

## Depending on a dropdown variable clicks the correct button (job queue, move to it's own class)
def checkAndRunDropdownInput(variable):
    if (variable.get() == "NDPPP predict.parset"):
        predict_clicked(buttons,
                        predict_btn,
                        calibrator_file_name,
                        predict_msout,
                        calibrator_nametag,
                        predict_sourcedb_output,
                        predict_solint,
                        predict_usebeammodel,
                        predict_onebeamperpatch,
                        predict_caltype
                        )
    elif (variable.get() == "NDPPP applycal.parset"):
        applycal_clicked(buttons,
                        applycal_btn,
                        MS_file_name,
                        applycal_msout,
                        applycal_datacolumn_in,
                        applycal_datacolumn_out,
                        calibrator_file_name,
                        applycal_updateweights
                        )
    elif (variable.get() == "NDPPP applybeam.parset"):
        applybeam_clicked(buttons,
                        applybeam_btn,
                        MS_file_name,
                        applybeam_msout,
                        applybeam_datacolumn_in,
                        applybeam_datacolumn_out,
                        applybeam_updateweights
                        )
    elif (variable.get() == "wsclean"):
        wsclean_clicked(buttons,
                        wsclean_btn,
                        config_file_name,
                        bool_vars,
                        MS_file_name,
                        MS_id,
                        time_format_variable
                        )

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

def darklightmodeswitch(menu, info_text, terminal_log):
    if darklightmode.get() == "Dark mode":
        darklightmode.set("Light mode")
        info_text.setDarkMode()
        terminal_log.setDarkMode()
    else:
        darklightmode.set("Dark mode")
        info_text.setLightMode()
        terminal_log.setLightMode()
    menu.entryconfigure(4, label=darklightmode.get())

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

# Options included in the predict.parset file
predict_solint = StringVar(root, "4")
calibrator_nametag = StringVar(root, "VirA")
predict_sourcedb_output = StringVar(root, "Ateam_LBA_CC.sourcedb")
predict_caltype = StringVar(root, "diagonal")
predict_onebeamperpatch = BooleanVar(root, True)
predict_usebeammodel = BooleanVar(root, True)
predict_msout = StringVar(root, ".")

# Options included in the applycal.parset file
applycal_datacolumn_in = StringVar(root, "DATA")
applycal_datacolumn_out = StringVar(root, "CORR_NO_BEAM")
applycal_parmdb = StringVar(root, "/instrument")
applycal_updateweights = BooleanVar(root, True)
applycal_msout = StringVar(root, ".")

# Options included in the applybeam.parset file
applybeam_datacolumn_in = StringVar(root, "CORR_NO_BEAM")
applybeam_datacolumn_out = StringVar(root, "CORRECTED_DATA")
applybeam_updateweights = BooleanVar(root, True)
applybeam_msout = StringVar(root, ".")

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
calibrator_name = StringVar(root, "Virgo")
skymodel_input_path = StringVar(root, "Ateam_LBA_CC.skymodel.txt")
skymodel_input = StringVar(root, "Ateam_LBA_CC.skymodel.txt")

time_format_variable = StringVar(root, "%Y-%m-%d %H:%M:%S")

MS_input_variable = StringVar(root, "ID_SB_uv.dppp.MS")

darklightmode = StringVar(root, "Dark mode")

# Coloring options
main_color = 'white'
frame_color = 'grey'

main_font = "Times"
secondary_font = "Courier"

# Basic configuration of the main window
root.title("LOFAR GUI 1.0f")
root.config(bg=main_color)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

main_row_ind = -1

# The "Left" side of the main window
left_frame = Frame(root, width=620, bg=frame_color)
left_frame.grid(row=0, column=0, columnspan=1, rowspan=2, sticky=W+S+E+N, padx=(4, 2), pady=4)
left_frame.grid_propagate(False)

# Ties the "View" and "Change" buttons together
left_frame.columnconfigure(0, weight=0)
left_frame.columnconfigure(1, weight=0)
left_frame.columnconfigure(2, weight=0)
left_frame.columnconfigure(3, weight=0)

lofar_title = Label(left_frame, text="LOFAR Imaging Tool", font=(main_font, 22, "bold"), bg=frame_color)
main_row_ind += 1
lofar_title.grid(row=main_row_ind, column=0, columnspan=3, sticky=W+N, pady=(40, 35), padx=(50, 5))

# The "Right" side of the main window
right_frame = Frame(root, background=frame_color)
right_frame.grid(row=0, column=1, columnspan=2, sticky=W+E+S+N, padx=(2, 4), pady=(4, 2))
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(1, weight=1)

# The "Bottom right" frame
right_bottom_frame = Frame(root, bg=frame_color)
right_bottom_frame.grid(row=1, column=1, columnspan=2, sticky=W+E+S+N, padx=(2, 4), pady=(2, 4))
right_bottom_frame.columnconfigure(0, weight=1)
right_bottom_frame.rowconfigure(1, weight=1)

# The top menu bar of the main window
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=change_fits)
filemenu.add_command(label="Load", command=load_clicked)
filemenu.add_command(label="Save", command=save_clicked)
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
settingsmenu.add_command(label="Wsclean", command= lambda: manage_config_clicked( root,
                                                            bool_vars,
                                                            config_file_name
                                                            ))
settingsmenu.add_command(label="Predict", command= lambda: manage_predict_clicked( root,
                                                            predict_msout,
                                                            predict_solint,
                                                            calibrator_nametag,
                                                            predict_sourcedb_output,
                                                            predict_caltype,
                                                            predict_usebeammodel,
                                                            predict_onebeamperpatch
                                                            ))
settingsmenu.add_command(label="Applycal", command= lambda: manage_applycal_clicked( root,
                                                            applycal_msout,
                                                            applycal_datacolumn_in,
                                                            applycal_datacolumn_out,
                                                            applycal_parmdb,
                                                            applybeam_updateweights
                                                            ))
settingsmenu.add_command(label="Applybeam", command= lambda: manage_applybeam_clicked( root,
                                                            applybeam_msout,
                                                            applybeam_datacolumn_in,
                                                            applybeam_datacolumn_out,
                                                            applybeam_updateweights
                                                            ))
settingsmenu.add_command(label=darklightmode.get(), command= lambda: darklightmodeswitch(settingsmenu, info_text, terminal_log))
menubar.add_cascade(label="Settings", menu=settingsmenu)

commandmenu = Menu(menubar, tearoff=0)
commandmenu.add_command(label="Job queue", command=job_queue_clicked)
menubar.add_cascade(label="Commands", menu=commandmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

view_column=1
view_width=5

# Displaying the files we're working on

main_row_ind+=1
file_info_label = Label(left_frame, text="Input data:", font=(main_font, 15, "bold"), bg=frame_color)
file_info_label.grid(row=main_row_ind, column=0, columnspan=2, sticky = W + N, pady=(10, 10), padx=(80, 0))

def change_input_skymodel():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a file",
                                            filetypes = (("Text files", "*.txt"),
                                                        (".skymodel files", "*.skymodel"),
                                                        ("all files", "*")))

    if not filename:
        info_text.writeToFeed("Change the sourcedb file: No file chosen \n")
    else:
        skymodel_input_path.set(filename)

        filename = os.path.basename(filename)

        skymodel_input.set(filename)
        skymodel_input_name_label.update()

        if proceed_warning_message("", "Should a new sourcedb file be created for this skymodel file?"):
            try:
                make_sourcedb(skymodel_input.get(), predict_sourcedb_output.get())
            except (OSError, KeyboardInterrupt):
                print("Error in making a new sourcedb, make sure you're inside the LOFAR environment\n")


skymodel_input_label = Label(left_frame, text="Sky model: ", font=(main_font, 11), bg=frame_color)
main_row_ind += 1
skymodel_input_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(5, 0), padx=(80, 0))

view_skymodel_btn = Button(left_frame, text="View", command= lambda: skymodel_contents(skymodel_input_path, info_text), width=view_width)
view_skymodel_btn.grid(row=main_row_ind, column=view_column + 1, padx=1, pady=(0,0), sticky=W)
change_skymodel_btn = Button(left_frame, text="Load", command=change_input_skymodel, width=view_width)
change_skymodel_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(0,0))

skymodel_input_name_label = Label(left_frame, textvariable=skymodel_input, font=(secondary_font, 11), bg=frame_color)
main_row_ind += 1
skymodel_input_name_label.grid(row=main_row_ind, column=0, columnspan=3, sticky = W + N, pady=(0, 5), padx=(80, 5))

# Change/View the calibrator .MS file

calibrator_file_label = Label(left_frame, text="Calibrator measurement set: ", font=(main_font, 11), bg=frame_color)
main_row_ind+=1
calibrator_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(5, 0), padx=(80, 0))

view_calibrator_btn = Button(left_frame, text="View", width=view_width,
                                command= lambda: view_calibrator_clicked(buttons, view_calibrator_btn, info_text, calibrator_file_name))
view_calibrator_btn.grid(row=main_row_ind, column=view_column + 1, padx=1, pady=(2,0), sticky=W)

change_open = BooleanVar(root, False)

def change_calibrator(index, MS_input_string):
    if change_open.get() == False:
        change_open.set(True)
        calibrator_id_entry_feed = Entry(left_frame, text="Calibrator ID", font=(main_font, 9), width=8)
        calibrator_id_entry_feed.delete(0, 'end')
        calibrator_id_entry_feed.grid(row=index, column=1, padx=(2, 1), pady=(4,5), sticky=W)
        calibrator_id_entry_feed.insert(0, "ID:")
        calibrator_id_entry_feed.config(fg='grey')

        calibrator_SB_entry_feed = Entry(left_frame, text="Calibrator Subband", font=(main_font, 9), width=8)
        calibrator_SB_entry_feed.delete(0, 'end')
        calibrator_SB_entry_feed.grid(row=index, column=2, padx=(0, 4), pady=(4,5), sticky=W)
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
            calibrator_id_entry_feed.grid(row=index, column=1, columnspan=2, padx=(5, 5), pady=(2,5))
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
            calibrator_id_entry_feed.grid(row=index, column=1, columnspan=2, padx=(5, 5), pady=(2,5))
            calibrator_id_entry_feed.delete(0, 'end')
            calibrator_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_calibrator(txt):
                calibrator_file_name.set(calibrator_id_entry_feed.get())
                calibrator_id.set(calibrator_id_entry_feed.get())
                calibrator_id_entry_feed.grid_remove()
                change_open.set(False)

            calibrator_id_entry_feed.bind("<Return>", handle_enter_calibrator)

    else:
        info_text.writeToFeed("Press enter to close the change window\n")

change_calibrator_btn = Button(left_frame, text="Load", command= lambda: change_calibrator(5, MS_input_variable.get()), width=view_width)
change_calibrator_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(2,0))

buttons.append(view_calibrator_btn)
buttons.append(change_calibrator_btn)

calibrator_file_name_label = Label(left_frame, textvariable=calibrator_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind += 1
calibrator_file_name_label.grid(row=main_row_ind, column=0, columnspan=3, sticky = W + N, pady=(0, 5), padx=(80, 5))

#############################################
# Change/View .MS file

MS_file_label = Label(left_frame, text="Solar MS: ", font=(main_font, 11), bg=frame_color)
main_row_ind+=1
MS_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(5, 0), padx=(80, 0))

view_MS_btn = Button(left_frame, text="View", width=view_width,
                    command= lambda: view_MS_clicked(buttons, view_MS_btn, info_text, MS_file_name))
view_MS_btn.grid(row=main_row_ind, column=view_column + 1, padx=1, pady=(2,0), sticky=W)

buttons.append(view_MS_btn)

change_MS_open = BooleanVar(root, False)

def change_MS(index, MS_input_string):
    if change_MS_open.get() == False:
        change_MS_open.set(True)
        MS_id_entry_feed = Entry(left_frame, text="Solar MS ID", font=(main_font, 9), width=8)
        MS_id_entry_feed.delete(0, 'end')
        MS_id_entry_feed.grid(row=index, column=1, padx=(2, 1), pady=(4,5), sticky=W)
        MS_id_entry_feed.insert(0, "ID:")
        MS_id_entry_feed.config(fg='grey')

        MS_SB_entry_feed = Entry(left_frame, text="Solar MS Subband", font=(main_font, 9), width=8)
        MS_SB_entry_feed.delete(0, 'end')
        MS_SB_entry_feed.grid(row=index, column=2, padx=(0, 4), pady=(4,5), sticky=W)
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
            MS_id_entry_feed.grid(row=index, column=1, columnspan=2, padx=(5, 5), pady=(2,5))
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
            MS_id_entry_feed.grid(row=index, column=1, columnspan=2, padx=(5, 5), pady=(2,5))
            MS_id_entry_feed.delete(0, 'end')
            MS_id_entry_feed.insert(0, "MS file name:")

            def handle_enter_MS(txt):
                MS_file_name.set(MS_id_entry_feed.get())
                MS_id.set(MS_id_entry_feed.get())
                MS_id_entry_feed.grid_remove()
                change_MS_open.set(False)

            MS_id_entry_feed.bind("<Return>", handle_enter_MS)

    else:
        info_text.writeToFeed("Press enter to close the change MS window\n")

change_MS_btn = Button(left_frame, text="Load", command= lambda: change_MS(7, MS_input_variable.get()), width=view_width)
change_MS_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(2,0))

MS_file_name_label = Label(left_frame, textvariable=MS_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind += 1
MS_file_name_label.grid(row=main_row_ind, column=0, columnspan=3, sticky = W + N, pady=(0, 5), padx=(80, 5))

buttons.append(change_MS_btn)

########################################

main_row_ind += 1
main_row_ind += 1

###########################################
# Calibrating data tab

calibrating_title = Label(left_frame, text="Calibrating data:", font=(main_font, 15, "bold"), bg=frame_color)
main_row_ind += 1
calibrating_title.grid(row=main_row_ind, column=0, columnspan=2, sticky = W + N, pady=(15, 10), padx=(80, 5))

main_row_ind += 1

calibrator_nametag_label = Label(left_frame, text="Calibrator:", font=(main_font, 11), bg=frame_color)
calibrator_nametag_entry = Entry(left_frame, text="VirA", font=(main_font, 11), width=20)
calibrator_nametag_entry.insert(0, "VirA")
calibrator_nametag_entry.config(fg='grey')

main_row_ind+=1
calibrator_nametag_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 0))
calibrator_nametag_entry.grid(row=main_row_ind, column=1, columnspan=3, sticky = W+N, pady=4, padx=(0, 5))

def handle_focus_in_nametag(_):
    calibrator_nametag_entry.delete(0, 'end')
    calibrator_nametag_entry.insert(0, calibrator_nametag.get())
    calibrator_nametag_entry.config(fg='black')

def handle_focus_out_nametag(_):
    calibrator_nametag_entry.delete(0, 'end')
    calibrator_nametag_entry.insert(0, calibrator_nametag.get())
    calibrator_nametag_entry.config(fg='grey')

def handle_enter_nametag(txt):
    calibrator_nametag.set(calibrator_nametag_entry.get())
    handle_focus_out_nametag("dummy")

def handle_key_press_nametag(txt):
    calibrator_nametag_entry.config(fg='black')

calibrator_nametag_entry.bind("<Key>", handle_key_press_nametag)
calibrator_nametag_entry.bind("<FocusIn>", handle_focus_in_nametag)
calibrator_nametag_entry.bind("<FocusOut>", handle_focus_out_nametag)
calibrator_nametag_entry.bind("<Return>", handle_enter_nametag)

sourcedb_output_label = Label(left_frame, text="Sourcedb file: ", font=(main_font, 11), bg=frame_color)
main_row_ind += 1
sourcedb_output_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=5, padx=(80, 0))

sourcedb_output_entry = Entry(left_frame, text="Ateam_LBA_CC.sourcedb", font=(main_font, 11), width=20)
sourcedb_output_entry.insert(0, predict_sourcedb_output.get())
sourcedb_output_entry.config(fg='grey')
sourcedb_output_entry.grid(row=main_row_ind, column=1, columnspan=3, sticky = W+N, pady=4, padx=(0, 5))

def handle_focus_in_sourcedb(_):
    sourcedb_output_entry.delete(0, 'end')
    sourcedb_output_entry.insert(0, predict_sourcedb_output.get())
    sourcedb_output_entry.config(fg='black')

def handle_focus_out_sourcedb(_):
    sourcedb_output_entry.delete(0, 'end')
    sourcedb_output_entry.insert(0, predict_sourcedb_output.get())
    sourcedb_output_entry.config(fg='grey')

def handle_enter_sourcedb(txt):
    predict_sourcedb_output.set(sourcedb_output_entry.get())
    handle_focus_out_sourcedb("dummy")

def handle_key_press_sourcedb(txt):
    sourcedb_output_entry.config(fg='black')

sourcedb_output_entry.bind("<Key>", handle_key_press_sourcedb)
sourcedb_output_entry.bind("<FocusIn>", handle_focus_in_sourcedb)
sourcedb_output_entry.bind("<FocusOut>", handle_focus_out_sourcedb)
sourcedb_output_entry.bind("<Return>", handle_enter_sourcedb)

col2_row_ind = main_row_ind

commands_btn_width=23

command_btns_index = main_row_ind

make_info_buttons(left_frame, command_btns_index, root)

predict_btn = Button(left_frame, text="NDPPP predict.parset", width=commands_btn_width,
                        command= lambda: predict_clicked(buttons,
                                                        predict_btn,
                                                        calibrator_file_name,
                                                        predict_msout,
                                                        calibrator_nametag,
                                                        predict_sourcedb_output,
                                                        predict_solint,
                                                        predict_usebeammodel,
                                                        predict_onebeamperpatch,
                                                        predict_caltype
                                                        ))
main_row_ind += 1
predict_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 0))
buttons.append(predict_btn)

view_predict_btn = Button(left_frame, text="View", width=view_width,
                command= lambda: view_predict_clicked(  calibrator_file_name,
                                                        predict_msout,
                                                        calibrator_nametag,
                                                        predict_sourcedb_output,
                                                        predict_solint,
                                                        predict_usebeammodel,
                                                        predict_onebeamperpatch,
                                                        predict_caltype,
                                                        info_text
                                                        ))
view_predict_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=1)
buttons.append(view_predict_btn)

def kill_predict_clicked():
    x = 0

kill_predict_btn = Button(left_frame, text="Kill", command=kill_predict_clicked, width=view_width)
kill_predict_btn.grid(row=main_row_ind, column=2, sticky = W, pady=3, padx=(0, 1))

applycal_btn = Button(left_frame, text="NDPPP applycal.parset", width=commands_btn_width,
                        command= lambda: applycal_clicked(buttons,
                                                        applycal_btn,
                                                        MS_file_name,
                                                        applycal_msout,
                                                        applycal_datacolumn_in,
                                                        applycal_datacolumn_out,
                                                        calibrator_file_name,
                                                        applycal_updateweights
                                                        ))
main_row_ind += 1
applycal_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 0))
buttons.append(applycal_btn)

view_applycal_btn = Button(left_frame, text="View", width=view_width,
                            command= lambda: view_applycal_clicked(MS_file_name,
                                                            applycal_msout,
                                                            applycal_datacolumn_in,
                                                            applycal_datacolumn_out,
                                                            calibrator_file_name,
                                                            applycal_updateweights,
                                                            info_text
                                                            ))
view_applycal_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=1)
buttons.append(view_applycal_btn)

def kill_applycal_clicked():
    x = 0

kill_applycal_btn = Button(left_frame, text="Kill", command=kill_applycal_clicked, width=view_width)
kill_applycal_btn.grid(row=main_row_ind, column=2, sticky = W, pady=3, padx=(0, 1))

applybeam_btn = Button(left_frame, text="NDPPP applybeam.parset", width=commands_btn_width,
                        command= lambda: applybeam_clicked(buttons,
                                                        applybeam_btn,
                                                        MS_file_name,
                                                        applybeam_msout,
                                                        applybeam_datacolumn_in,
                                                        applybeam_datacolumn_out,
                                                        applybeam_updateweights
                                                        ))
main_row_ind += 1
applybeam_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 0))
buttons.append(applybeam_btn)

view_applybeam_btn = Button(left_frame, text="View", width=view_width,
                        command= lambda: view_applybeam_clicked(MS_file_name,
                                                        applybeam_msout,
                                                        applybeam_datacolumn_in,
                                                        applybeam_datacolumn_out,
                                                        applybeam_updateweights,
                                                        info_text
                                                        ))
view_applybeam_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=1)
buttons.append(view_applybeam_btn)

def kill_applybeam_clicked():
    x = 0

kill_applybeam_btn = Button(left_frame, text="Kill", command=kill_applybeam_clicked, width=view_width)
kill_applybeam_btn.grid(row=main_row_ind, column=2, sticky = W, pady=3, padx=(0, 1))

#######################################

#######################################
# The Imaging tab

imaging_title = Label(left_frame, text="Imaging:", font=(main_font, 15, "bold"), bg=frame_color)
main_row_ind += 1
imaging_title.grid(row=main_row_ind, column=0, columnspan=2, sticky = W + N, pady=(25, 5), padx=(80, 5))

config_file_label = Label(left_frame, text="Configuration file: ", font=(main_font, 11), bg=frame_color)
main_row_ind+=1
config_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(5,0), padx=(80, 0))

# Change config files
def change_config():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a file",
                                            filetypes = (("Text files", "*.txt"),
                                                        ("all files", "*")))

    if not filename:
        info_text.writeToFeed("Change the config file: No file chosen \n")
    else:
        config_file_path.set(filename)

        filename = os.path.basename(filename)

        config_file_name.set(filename)
        config_file_name_label.update()

change_config_btn = Button(left_frame, text="Load", command=change_config, width=view_width)
change_config_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(2,0))

view_config_btn = Button(left_frame, text="View", command= lambda: print_config(config_file_path.get(), width=view_width)
view_config_btn.grid(row=main_row_ind, column=view_column + 1, padx=1, pady=(2,0), sticky=W)

buttons.append(view_config_btn)

config_file_name_label = Label(left_frame, textvariable=config_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
config_file_name_label.grid(row=main_row_ind, column=0, columnspan=2, sticky = W + N, pady=(0, 5), padx=(80, 5))

#####################################

wsclean_btn = Button(left_frame, text="wsclean", width=commands_btn_width,
                    command= lambda: wsclean_clicked(buttons,
                                                    wsclean_btn,
                                                    config_file_name,
                                                    bool_vars,
                                                    MS_file_name,
                                                    MS_id,
                                                    time_format_variable
                                                    ))
main_row_ind += 1
wsclean_btn.grid(row=main_row_ind, column=0, sticky = W+N, pady=3, padx=(70, 0))
buttons.append(wsclean_btn)

view_wsclean_btn = Button(left_frame, text="View", width=view_width,
                            command= lambda: view_wsclean_clicked(
                            config_file_name,
                            bool_vars,
                            MS_file_name
                            ))
view_wsclean_btn.grid(row=main_row_ind, column=1, sticky = W+N, pady=3, padx=1)
buttons.append(view_wsclean_btn)

# Plotting and visualization
#############################################
visualization_label = Label(left_frame, text="Data handling:", font=(main_font, 15, "bold"), bg=frame_color)
main_row_ind += 1
visualization_label.grid(row=main_row_ind, column=0, columnspan=2, sticky = W + N, pady=(20, 5), padx=(80, 5))

# View single .fits file

fits_file_label = Label(left_frame, text="Plotting FITS: ", font=(main_font, 11), bg=frame_color)
main_row_ind+=1
fits_file_label.grid(row=main_row_ind, column=0, sticky = W + N, pady=(5, 0), padx=(80, 0))

change_fits_btn = Button(left_frame, text="Load", command=change_fits, width=view_width)
change_fits_btn.grid(row=main_row_ind, column=view_column, padx=1, pady=(2,0))

view_fits_btn = Button(left_frame, text="View", command= lambda: plot_single_fits(fits_file_path.get()), width=view_width)
view_fits_btn.grid(row=main_row_ind, column=view_column + 1, padx=1, pady=(2,0), sticky=W)

fits_file_name_label = Label(left_frame, textvariable=fits_file_name, font=(secondary_font, 11), bg=frame_color)
main_row_ind+=1
fits_file_name_label.grid(row=main_row_ind, column=0, columnspan=3, sticky = W + N, pady=(0, 5), padx=(80, 5))

buttons.append(view_fits_btn)
buttons.append(change_fits_btn)

## Runs a coordinate transformation
def coord_clicked():
    filename = fits_file_path.get()

    if not filename:
        info_text.writeToFeed("No file chosen for coordinate transformation \n")
    else:
        icrs_to_helio(filename)

main_row_ind += 1
coord_btn = Button(left_frame, text="Run a coordinate transformation", command=coord_clicked, width=25, state='disabled')
coord_btn.grid(row=main_row_ind, column=0, sticky = W+N, padx=(70, 5), pady=(10, 3))

buttons.append(coord_btn)

def multiple_plot_clicked():
    filez = filedialog.askopenfilenames(initialdir = os.getcwd(),
                                            title="Select files",
                                            filetypes = ((".fits files", "*.fits"),
                                                        ("all files", "*")))

    lst = list(filez)
    index = 0
    if len(lst) == 0:
        info_text.writeToFeed("No file(s) chosen \n")
    else:
        lst = list(filez)
        index = 0
        for f in lst:
            #f = os.path.basename(f)
            save_fits(f, index)
            index = index + 1
        print("Plotting multiple files \n")

plot_many_btn = Button(left_frame, text="Plot & save multiple .fits files", width=25, command=multiple_plot_clicked)
main_row_ind += 1
plot_many_btn.grid(row=main_row_ind, column=0, sticky = N + W, padx=(70, 5), pady=3)

buttons.append(plot_many_btn)

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
        info_text.writeToFeedFeed("No file(s) chosen \n")

video_btn = Button(left_frame, text="Wrap multiple plots into a video", width=25, command=video_clicked, state='disabled')
main_row_ind += 1
video_btn.grid(row=main_row_ind, column=0, sticky = N + W, padx=(70, 5), pady=3)

############################################

# Text box for an information feed
info_text = TextBox(right_frame, "Information feed", 37, 70)
info_text.addHighlightTextEntry()

# Text box for the terminal feed information
terminal_log = TextBox(right_bottom_frame, "Terminal log", 23, 70)
terminal_log.enableTerminalRedirect()

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
