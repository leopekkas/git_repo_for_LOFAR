## @file Load.py
# @brief Loading the state of the program from a savefile

import tkFileDialog as filedialog
import os
## Loads the values from a save file into the StringVars in the main program
def LoadNewValues(skymodel, calibratorMS, solarMS, calibrator, sourcedb, configfile, fitsfile):
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                            title="Select a file",
                                            filetypes = (("Save files", "*.sav"),
                                                        ("all files", "*")))
    retList = []
    try:
        file = open(filename)
        retList = [line for line in file.readlines() if line.strip()]
        file.close()
    except (OSError, IOError, KeyboardInterrupt):
        print("No save file present\n")
        return -1

    skymodel.set(retList[0].strip())
    solarMS.set(retList[1].strip())
    calibratorMS.set(retList[2].strip())
    calibrator.set(retList[3].strip())
    sourcedb.set(retList[4].strip())
    fitsfile.set(retList[5].strip())
    for i in range(3, len(retList)):
        if "Predict file" in retList[i]:
            i += 1
            predictfile = open("predict.parset", "w")
            for j in range(i, len(retList)):
                if "Applycal file" in retList[j]:
                    break
                else:
                    predictfile.write(retList[j])
            predictfile.close()
        if "Applycal file" in retList[i]:
            i += 1
            applycalfile = open("applycal.parset", "w")
            for k in range(i, len(retList)):
                if "Applybeam file" in retList[k]:
                    break
                else:
                    applycalfile.write(retList[k])
            applycalfile.close()
        if "Applybeam file" in retList[i]:
            i += 1
            applybeamfile = open("applybeam.parset", "w")
            for ii in range(i, len(retList)):
                if "Config file" in retList[ii]:
                    break
                else:
                    applybeamfile.write(retList[ii])
            applybeamfile.close()
        if "Config file" in retList[i]:
            i += 1
            configurationfile = open(configfile.get(), "w")
            for jj in range(i, len(retList)):
                configurationfile.write(retList[jj])
            configurationfile.close()
