from Tkinter import Toplevel, Frame, Label, N, S, E, W
from UI_helper_functions import setUpPredictEntries, setUpApplycalEntries
from UI_helper_functions import setUpApplybeamEntries, setUpCheckbuttons

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
