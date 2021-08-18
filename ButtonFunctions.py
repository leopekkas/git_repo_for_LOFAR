import sys
sys.path.insert(1, 'StateManager')
import subprocess as sub

from Save import Save
from Load import LoadNewValues
from File_reader import make_predict_file, make_applycal_file, make_applybeam_file, print_skymodel, read_config
from File_reader import lines_in_wsclean
from UI_helper_functions import disableButtons, enableButtons

## Click function for loading a new state into the program
def load_clicked(skymodel_input, calibrator_file_name, MS_file_name, calibrator_nametag,
    predict_sourcedb_output, config_file_name, fits_file_name
    ):
    LoadNewValues(skymodel_input, calibrator_file_name, MS_file_name, calibrator_nametag, predict_sourcedb_output, config_file_name, fits_file_name)

## Click function for saving the current state, creates a new Save class object
def save_clicked(skymodel_input, MS_file_name, calibrator_file_name, calibrator_nametag,
    predict_sourcedb_output, config_file_name, fits_file_name
    ):
    newsavefile = Save(skymodel_input.get(), MS_file_name.get(), calibrator_file_name.get(), calibrator_nametag.get(), predict_sourcedb_output.get(),
        "predict.parset", "applycal.parset", "applybeam.parset", config_file_name.get(), fits_file_name.get())
    newsavefile.saveToSaveFile()

## Click function for the NDPPP predict.parset command
def predict_clicked(buttons, predict_btn, calibrator_file_name, predict_msout, calibrator_nametag,
    predict_sourcedb_output, predict_solint, predict_usebeammodel, predict_onebeamperpatch, predict_caltype):
    disableButtons(buttons)
    predict_btn.update()

    make_predict_file(calibrator_file_name.get(), predict_msout.get(), calibrator_nametag.get(),
                    predict_sourcedb_output.get(), predict_solint.get(), predict_usebeammodel.get(),
                    predict_onebeamperpatch.get(), predict_caltype.get())

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

## Click function for the NDPPP applycal.parset command
def applycal_clicked(buttons, applycal_btn, MS_file_name, applycal_msout, applycal_datacolumn_in,
    applycal_datacolumn_out, calibrator_file_name, applycal_updateweights
    ):
    disableButtons(buttons)
    applycal_btn.update()

    make_applycal_file(MS_file_name.get(), applycal_msout.get(), applycal_datacolumn_in.get(), applycal_datacolumn_out.get(), calibrator_file_name.get(), applycal_updateweights.get())

    try:
        # Run NDPPP applycal.parset here
        p = sub.call(["NDPPP", "applycal.parset"])
        print("NDPPP applycal.parset \n")
    except (OSError, KeyboardInterrupt):
        print("Error in running NDPPP applycal.parset \n")
        applycal_btn.update()
        enableButtons(buttons)

    applycal_btn.update()
    enableButtons(buttons)

## Click function for the NDPPP applybeam.parset command (move to its own class)
def applybeam_clicked(buttons, applybeam_btn, MS_file_name, applybeam_msout,
    applybeam_datacolumn_in, applybeam_datacolumn_out, applybeam_updateweights
    ):
    disableButtons(buttons)
    applybeam_btn.update()

    make_applybeam_file(MS_file_name.get(), applybeam_msout.get(), applybeam_datacolumn_in.get(), applybeam_datacolumn_out.get(), applybeam_updateweights.get())

    try:
        # Run NDPPP applybeam.parset here
        p = sub.call(["NDPPP", "applybeam.parset"])
        print("NDPPP applybeam.parset \n")
    except (OSError, KeyboardInterrupt):
        print("Error in running NDPPP applybeam.parset \n")
        applybeam_btn.update()
        enableButtons(buttons)

    applybeam_btn.update()
    enableButtons(buttons)

## Click function for wsclean command
def wsclean_clicked(buttons, wsclean_btn, config_file_name, bool_vars, MS_file_name, MS_id, time_format_variable):
    try:
        disableButtons(buttons)
        wsclean_btn.update()
        wscommand = read_config(config_file_name.get(), bool_vars, MS_file_name, MS_id, time_format_variable)
        if wscommand==-1:
            # Do nothing
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

## Switches the terminal color between dark and light
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

## Prints the contents of the skymodel file
def skymodel_contents(skymodel_input_path, info_text):
    print_skymodel(skymodel_input_path.get(), info_text)

## Prints the contents of the configuration file
#
# @param filename The configuration file in String format
# @param textfield The Tkinter Text widget that the information will be written into
def print_config(filename, textfield):
    try:
        file = open(filename)
        textfield.insert('end', "The config file contains the following options: \n")
        lines = [line for line in file.readlines() if line.strip()]
        for l in lines:
            textfield.insert('end', l)

        file.close()
        textfield.writeToFeed("")
    except IOError:
        textfield.writeToFeed("No configuration file with the name \"" + os.path.basename(filename) + "\" found")

## Prints the contents of the calibrator MS file into the information feed
def view_calibrator_clicked(buttons, view_calibrator_btn, info_text, calibrator_file_name):
    disableButtons(buttons)
    view_calibrator_btn.update()

    try:
        second_command = "in=" + calibrator_file_name.get()
        p = sub.Popen(["msoverview", second_command], stdout=sub.PIPE)
        for line in p.stdout:
            info_text.writeToFeedNoLinebreak(line)
        info_text.writeToFeed("")
        view_calibrator_btn.update()
        enableButtons(buttons)

    except (OSError, KeyboardInterrupt):
        info_text.writeToFeed("Error in reading the .MS-file contents")
        view_calibrator_btn.update()
        enableButtons(buttons)

## Prints the contents of the MS file into the information feed
def view_MS_clicked(buttons, view_MS_btn, info_text, MS_file_name):
    disableButtons(buttons)
    view_MS_btn.update()
    try:
        second_command = "in=" + MS_file_name.get()
        full_command = "msoverview in=" + MS_file_name.get()
        output_file = open("msoverview_output.txt", "w")
        p = sub.Popen(["msoverview", second_command], stdout=sub.PIPE)
        for line in p.stdout:
            output_file.write(line)
            info_text.writeToFeedNoLinebreak(line)
        info_text.writeToFeed("")
        output_file.close()
        view_MS_btn.update()
        enableButtons(buttons)

    except (OSError, KeyboardInterrupt):
        info_text.writeToFeed("Error in reading the .MS-file contents")
        view_MS_btn.update()
        enableButtons(buttons)

## Prints out the contents of the predict.parset file
def view_predict_clicked(calibrator_file_name, predict_msout, calibrator_nametag,
    predict_sourcedb_output, predict_solint, predict_usebeammodel, predict_onebeamperpatch, predict_caltype, info_text):

    make_predict_file(calibrator_file_name.get(), predict_msout.get(), calibrator_nametag.get(), predict_sourcedb_output.get(), predict_solint.get(), predict_usebeammodel.get(), predict_onebeamperpatch.get(), predict_caltype.get())
    if os.path.exists(os.getcwd() + "/predict.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("predict.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the predict.parset contents \n")
    else:
        print("Error, no predict.parset found in the working directory \n")

## Prints out the contents of the applycal.parset file
def view_applycal_clicked(MS_file_name, applycal_msout, applycal_datacolumn_in,
    applycal_datacolumn_out, calibrator_file_name, applycal_updateweights, info_text):
    make_applycal_file(MS_file_name.get(), applycal_msout.get(), applycal_datacolumn_in.get(), applycal_datacolumn_out.get(), calibrator_file_name.get(), applycal_updateweights.get())
    if os.path.exists(os.getcwd() + "/applycal.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("applycal.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the applycal.parset contents \n")
    else:
        print("Error, no applycal.parset found in the working directory \n")

## Prints out the contents of the applybeam.parset file
def view_applybeam_clicked(MS_file_name, applybeam_msout,
    applybeam_datacolumn_in, applybeam_datacolumn_out, applybeam_updateweights, info_text):
    make_applybeam_file(MS_file_name.get(), applybeam_msout.get(), applybeam_datacolumn_in.get(), applybeam_datacolumn_out.get(), applybeam_updateweights.get())
    if os.path.exists(os.getcwd() + "/applybeam.parset"):
        try:
            # Run NDPPP applycal.parset here
            print_parset("applybeam.parset", info_text)
        except (OSError, KeyboardInterrupt):
            print("Error in printing the applybeam.parset contents \n")
    else:
        print("Error, no applybeam.parset found in the working directory \n")

## Prints out the content of the wsclean command with current values
def view_wsclean_clicked(config_file_name, bool_vars, MS_file_name):
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

    print("\n")
