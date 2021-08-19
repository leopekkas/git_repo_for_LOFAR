## @file SettingWindows.py
# @brief In charge of building and managing the management windows for wsclean config etc.

from Tkinter import Toplevel, Frame, Label, N, S, E, W, Checkbutton, Entry
from UI_helper_functions_py2 import buildAnEntryBox

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

## Sets up the manage predict window
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

## Sets up the manage applycal window
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

## Sets up the manage applybeam window
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

## Starts up the predict.parset management window
def manage_predict_clicked(root, predict_msout, predict_solint, calibrator_nametag, predict_sourcedb_output, predict_caltype, predict_usebeammodel, predict_onebeamperpatch):
    main_font = "Times"

    predict_main_window = Toplevel(root)
    predict_main_window.title("predict.parset")
    predict_main_window.wm_attributes('-type', 'dialog')

    top_frame = Frame(predict_main_window)
    top_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)

    predict_frame = Frame(predict_main_window)
    predict_frame.grid(row=1, column=0, sticky=N+W, padx=5, pady=5)

    predict_window_title = Label(top_frame, text="Options in predict.parset", font=(main_font, 13, "bold"))
    predict_window_title.grid(row=0, column=0, padx=(20, 0), pady=20)

    setUpPredictEntries(predict_frame, predict_msout, predict_solint, calibrator_nametag, predict_sourcedb_output, predict_caltype, predict_usebeammodel, predict_onebeamperpatch)

## Starts up the applycal.parset management window
def manage_applycal_clicked(root, applycal_msout, applycal_datacolumn_in, applycal_datacolumn_out, applycal_parmdb, applybeam_updateweights):
    main_font = "Times"

    applycal_main_window = Toplevel(root)
    applycal_main_window.title("applycal.parset")
    applycal_main_window.wm_attributes('-type', 'dialog')

    top_frame = Frame(applycal_main_window)
    top_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)

    applycal_frame = Frame(applycal_main_window)
    applycal_frame.grid(row=1, column=0, sticky=N+W, padx=5, pady=5)

    applycal_window_title = Label(top_frame, text="Options in applycal.parset", font=(main_font, 13, "bold"))
    applycal_window_title.grid(row=0, column=0, padx=(20, 0), pady=20)

    setUpApplycalEntries(applycal_frame, applycal_msout, applycal_datacolumn_in, applycal_datacolumn_out, applycal_parmdb, applybeam_updateweights)

## Starts up the applybeam.parset management window
def manage_applybeam_clicked(root, applybeam_msout, applybeam_datacolumn_in, applybeam_datacolumn_out, applybeam_updateweights):
    main_font = "Times"

    applybeam_main_window = Toplevel(root)
    applybeam_main_window.title("applybeam.parset")
    applybeam_main_window.wm_attributes('-type', 'dialog')

    top_frame = Frame(applybeam_main_window)
    top_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)

    applybeam_frame = Frame(applybeam_main_window)
    applybeam_frame.grid(row=1, column=0, sticky=N+W, padx=5, pady=5)

    applybeam_window_title = Label(top_frame, text="Options in applybeam.parset", font=(main_font, 13, "bold"))
    applybeam_window_title.grid(row=0, column=0, padx=(20, 0), pady=20)

    setUpApplybeamEntries(applybeam_frame, applybeam_msout, applybeam_datacolumn_in, applybeam_datacolumn_out, applybeam_updateweights)

## Starts up the wsclean management window
def manage_config_clicked(root, bool_vars, config_file_name):
    main_font = "Times"

    config_main_window = Toplevel(root)
    config_main_window.title("wsclean")
    config_main_window.wm_attributes('-type', 'dialog')

    top_frame = Frame(config_main_window)
    top_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)

    config_window = Frame(config_main_window)
    config_window.grid(row=1, column=0, sticky=N+W, padx=5, pady=5)

    config_window_title = Label(top_frame, text="Options in wsclean", font=(main_font, 13, "bold"))
    config_window_title.grid(row=0, column=0, padx=(20, 0), pady=20)

    setUpCheckbuttons(config_window, bool_vars, config_file_name)
