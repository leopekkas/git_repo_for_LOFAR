import sys
import subprocess as sub
import os, errno
import shutil
from datetime import datetime, time, timedelta
from UI_helper_functions import proceed_warning_message
import csv

## Returns a list of all the lines in the wsclean command depending on the configuration settings
#
# @param myvars A dictionary with key - value pairs that match the config option to its value
# @param bool_vars List of variables that inform the program which options are included in the wsclean command and which are excluded
# @param input_set The input measurement set for the wsclean command (Solar MS)
# @param start_time Starting time of the wsclean command in computer steps
# @param end_time Ending time of the wsclean command in computer steps
#
# @return a list of all the parts of a wsclean command
def lines_in_wsclean(myvars, bool_vars, input_set, start_time, end_time):

    ws_list = []

    ws_list.append("wsclean")

    if (bool_vars[0].get() and myvars.has_key("cores")):
        ws_list.append("-j")
        ws_list.append(myvars["cores"])
    if (bool_vars[1].get() and myvars.has_key("memory_limit")):
        ws_list.append("-mem")
        ws_list.append(myvars["memory_limit"])
    if (bool_vars[2].get()):
        ws_list.append("-no-reorder")
    if (bool_vars[3].get()):
        ws_list.append("-no-update-model-required")
    if (bool_vars[4].get() and myvars.has_key("mgain")):
        ws_list.append("-mgain")
        ws_list.append(myvars["mgain"])
    if (bool_vars[5].get() and myvars.has_key("weight_briggs")):
        ws_list.append("-weight")
        ws_list.append("briggs")
        ws_list.append(myvars["weight_briggs"])
    if (bool_vars[6].get() and myvars.has_key("size")):
        ws_list.append("-size")
        ws_list.append(myvars["size"])
        if myvars.has_key("size2"):
            ws_list.append(myvars["size2"])
        else:
            # If only one size value is inserted, use the same value for size1 and size2
            ws_list.append(myvars["size"])
    if (bool_vars[7].get() and myvars.has_key("scale")):
        scale_string = myvars["scale"] + "asec"
        ws_list.append("-scale")
        ws_list.append(scale_string)
    if (bool_vars[8].get() and myvars.has_key("polarisation")):
        ws_list.append("-pol")
        ws_list.append(myvars["polarisation"])
    if (bool_vars[9].get() and myvars.has_key("auto_mask")):
        ws_list.append("-auto-mask")
        ws_list.append(myvars["auto_mask"])
    if (bool_vars[10].get()):
        ws_list.append("-multiscale")
    if (bool_vars[11].get() and myvars.has_key("auto_threshold")):
        ws_list.append("-auto-threshold")
        ws_list.append(myvars["auto_threshold"])
    if (bool_vars[12].get() and myvars.has_key("data_column")):
        ws_list.append("-data-column")
        ws_list.append(myvars["data_column"])
    if (bool_vars[13].get() and myvars.has_key("n_iter")):
        ws_list.append("-niter")
        ws_list.append(myvars["n_iter"])
    if (bool_vars[14].get() and myvars.has_key("intervals_out")):
        ws_list.append("-intervals-out")
        ws_list.append(myvars["intervals_out"])
    if (bool_vars[15].get() and myvars.has_key("start_time")):
        ws_list.append("-interval")
        ws_list.append(str(start_time))
        if myvars.has_key("end_time"):
            ws_list.append(str(end_time))
    if (bool_vars[16].get()):
        ws_list.append("-fit-beam")
    if (bool_vars[17].get()):
        ws_list.append("-make-psf")
    ws_list.append(input_set.get())

    ws_list_ret = [x.replace("\n", "") for x in ws_list]

    return ws_list_ret

## Receives an input and the desired format (YYYY-MM-DD HH:MM:SS) and checks if the input matches the format
#
# @param input The input value (String)
# @param format The format in which the datetime should be presented in the configuration
def check_if_datetime(input, format):
    try:
        datetime.strptime(input.strip(), format.get())
        return True
    except (ValueError, AttributeError):
        return False
    return True

## Reads the specified configuration file and changes the input datetimes to simulation steps,
## returns a list of commands included in the wsclean command
#
# @param filename The configuration file name
# @param bool_vars List of variables that inform the program which options are included in the wsclean command and which are excluded
# @oaram input_set The input measurement set (Solar MS)
# @param MS_id String variable of the solar MS ID
# @param time_format Desired time format for datetime objects in wsclean
#
# @return List of wsclean options that are comprised by the whole wsclean command
def read_config(filename, bool_vars, input_set, MS_id, time_format):
    MS_info_dict = {}

    try:
        MS_info_dict = read_MS_info(MS_info_dict)
    except IOError:
        print("No file called \"MS_info.csv\" found, using timesteps in the wsclean command\n")

    # Fill a "myvars" dict with key - value pairs corresponding to configuration options
    myvars = {}
    try:
        with open(filename) as f:
            for line in f:
                name, value = line.partition("=")[::2]
                myvars[name.strip()] = str(value)
    except (OSError, IOError, KeyboardInterrupt):
        print("An error occured with reading the config file\n")
        return -1

    start_time = "01-01-2000 00:00:00"
    end_time = "01-01-2000 00:00:00"

    if myvars.has_key("start_time"):
        start_time = myvars["start_time"]
    if myvars.has_key("end_time"):
        end_time = myvars["end_time"]

    if MS_info_dict.has_key(MS_id.get()):
        MS_values = MS_info_dict[MS_id.get()]
        print("Reading time information for measurement set: " + MS_id.get() + "\n")
        MS_start_datetime = MS_values[0]
        MS_end_datetime = MS_values[1]
        total_steps = MS_values[2]
        if (check_if_datetime(start_time, time_format) and check_if_datetime(end_time, time_format)):
            print("Start time: " + MS_start_datetime + "\nEnd time:" + MS_end_datetime + "\nnsteps" + total_steps + "\n")
            start_time, end_time = calculate_real_time_into_steps(start_time, end_time, MS_start_datetime, MS_end_datetime, total_steps, time_format)
        else:
            print("Config file input is not in the format " + time_format.get() + ": " + str(start_time))
            return -1
    else:
        print("The file \"MS_info.csv\" doesn't contain an entry for the MS file: " + MS_id.get())
        return -1

    ws_list_ret = lines_in_wsclean(myvars, bool_vars, input_set, start_time, end_time)

    # Return a list of terminal inputs
    return ws_list_ret

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

## Prints the contents of the skymodel file
#
# @param filename The skymodel file in String format
# @param textfield The Tkinter Text widget that the information will be written into
def print_skymodel(filename, textfield):
    try:
        file = open(filename)
        textfield.insert('end', "The sourcedb file contains the following lines: \n")
        lines = [line for line in file.readlines() if line.strip()]
        for l in lines:
            textfield.insert('end', l)

        file.close()
        textfield.writeToFeed("", textfield)

    except IOError:
        textfield.writeToFeed("No configuration file with the name \"" + os.path.basename(filename) + "\" found")

## Prints the contents of the specified .parset file
#
# @param filename The predict.parset file in String format
# @param textfield The Tkinter Text widget that the information will be written into
def print_parset(filename, textfield):
    textfield.insert('end', "The " + filename + " file contains the following lines: \n")

    try:
        file = open(filename)
        lines = [line for line in file.readlines() if line.strip()]
        for l in lines:
            textfield.insert('end', l)

        file.close()
        textfield.writeToFeed("")
    except IOError:
        textfield.writeToFeed("No configuration file with the name \"" + os.path.basename(filename) + "\" found")

## Writes a predict.parset file
#
# @param msin The Solar MS
# @param msout Output file name ("." overwrites the msin file)
# @param source The gaincal.sources -option
# @param source_db The Source db option
# @param solint Solution interval (int/String)
# @param usebeammodel The usebeammodel option, Boolean value
# @param onebeamperpatch The onebeamperpatch option, Boolean value
# @param caltype Caltype option in wsclean
def make_predict_file(msin, msout, source, source_db, solint, usebeammodel, onebeamperpatch, caltype):
    predict_file = open("predict.parset", "w")
    predict_file.write("msin=" + msin + "\n")
    predict_file.write("msout=" + msout + "\n")
    predict_file.write("\nsteps=[gaincal]\n")
    predict_file.write("\ngaincal.usebeammodel=" + str(usebeammodel) + "\n")
    predict_file.write("gaincal.solint=" + str(solint) + "\n")
    predict_file.write("gaincal.sources=" + source + "\ngaincal.sourcedb=" + source_db + "\ngaincal.onebeamperpatch=" + str(onebeamperpatch) + "\n")
    predict_file.write("gaincal.caltype=" + caltype + "\n")
    predict_file.close()

## Writes an applycal.parset file
#
# @param msin The Solar MS
# @param msout Output file name ("." overwrites the msin file)
# @param datacolumn_in The datacolumn the command modifies
# @param datacolumn_out The datacolumn which containsthe calibrated values
# @param calibrator Calibrator MS
# @param updateweights The updateweights option, Boolean value
def make_applycal_file(msin, msout, datacolumn_in, datacolumn_out, calibrator, updateweights):
    applycal_file = open("applycal.parset", "w")
    applycal_file.write("msin=" + msin + "\n")
    applycal_file.write("msout=" + msout + "\n")
    applycal_file.write("msin.datacolumn=" + datacolumn_in + "\n")
    applycal_file.write("msout.datacolumn=" + datacolumn_out + "\n")
    applycal_file.write("steps=[applycal]\n\n")
    applycal_file.write("applycal.parmdb=" + calibrator + "/instrument\n")
    applycal_file.write("applycal.updateweights=" + str(updateweights) + "\n")
    applycal_file.close()

## Writes an applybeam.parset file
#
# @param msin The Solar MS
# @param msout Output file name ("." overwrites the msin file)
# @param datacolumn_in The datacolumn the command modifies
# @param datacolumn_out The datacolumn which containsthe calibrated values
# @param updateweights The updateweights option, Boolean value
def make_applybeam_file(msin, msout, datacolumn_in, datacolumn_out, updateweights):
    applybeam_file = open("applybeam.parset", "w")
    applybeam_file.write("msin=" + msin + "\n")
    applybeam_file.write("msout=" + msout + "\n")
    applybeam_file.write("msin.datacolumn=" + datacolumn_in + "\n")
    applybeam_file.write("msout.datacolumn=" + datacolumn_out + "\n")
    applybeam_file.write("steps=[applybeam]\n")
    applybeam_file.write("applybeam.updateweights=" + str(updateweights) + "\n")
    applybeam_file.close()

## Writes a new sourcedb file with LOFAR's "makesourcedb" command
#
# @param input Skymodel file
# @param output Name of the created sourcedb
def make_sourcedb(input, output):
    source_output = output
    input_string = "in=" + input
    output_string = "out=" + output

    current_path = os.getcwd()

    if output.endswith('.sourcedb'):
        # Check if prefix.sourcedb exists and remove it if it does
        if os.path.isdir(output):
            message = "Overlapping file names", "This sourcedb already exists in the working directory, continuing will overwrite it. \n\nDo you wish to proceed?"
            if proceed_warning_message(message):
                try:
                    shutil.rmtree(source_output)
                    print("Removed and wrote a new \'" + source_output  + "\' file \n")
                except OSError as e:
                    pass
                #pr = sub.call(["rm", sourcedb_string])
                p = sub.call(["makesourcedb", input_string, output_string])
                print("makesourcedb" + input_string + " " + output_string + "\n")
            else:
                print("No new .sourcedb file created\n")
        else:
            p = sub.call(["makesourcedb", input_string, output_string])
            print("makesourcedb" + input_string + " " + output_string + "\n")
    else:
        print("Please specify the filename with a \'.sourcedb\' extension \n")

## Calculates a datetime object into calculation steps used in wsclean
#
# @param start_datetime a Datetime object of the starting time
# @param end_datetime a Datetime object of the ending time
# @param ms_starttime The starting Datetime of the Solar MS in question
# @param ms_endtime Ending Datetime of the Solar MS
# @param nsteps The amount of images/steps in the Solar MS
# @param time_format The format used in the Datetime objects
def calculate_real_time_into_steps(start_datetime, end_datetime, ms_starttime, ms_endtime, nsteps, time_format):
    start_datetime_obj = datetime.strptime(start_datetime.strip(), time_format.get())
    end_datetime_obj = datetime.strptime(end_datetime.strip(), time_format.get())
    ms_starttime_obj = datetime.strptime(ms_starttime.strip(), time_format.get())
    ms_endtime_obj = datetime.strptime(ms_endtime.strip(), time_format.get())
    total_seconds = (ms_endtime_obj - ms_starttime_obj).days * 24 * 3600 + (ms_endtime_obj - ms_starttime_obj).seconds

    relative_seconds_start = (start_datetime_obj - ms_starttime_obj).days * 24 * 3600 + (start_datetime_obj - ms_starttime_obj).seconds
    relative_seconds_end = (end_datetime_obj - ms_starttime_obj).days * 24 * 3600 + (end_datetime_obj - ms_starttime_obj).seconds

    steps_to_seconds_ratio = float(nsteps)/int(total_seconds)

    start_stepvalue = int(steps_to_seconds_ratio * relative_seconds_start)
    end_stepvalue = int(steps_to_seconds_ratio * relative_seconds_end)

    x = start_stepvalue
    y = end_stepvalue
    return x, y
