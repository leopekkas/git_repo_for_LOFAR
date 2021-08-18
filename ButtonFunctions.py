import sys
sys.path.insert(1, 'StateManager')
import subprocess as sub

from Save import Save
from Load import LoadNewValues
from File_reader import make_predict_file, make_applycal_file, make_applybeam_file
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
