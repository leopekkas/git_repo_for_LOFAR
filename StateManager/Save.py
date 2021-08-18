from tkFileDialog import asksaveasfile

class Save:

    ## Class that holds the saved values
    def __init__(
        self, skymodel, solarMS, calibratorMS, calibrator, sourcedb, predictfile,
        applycalfile, applybeamfile, configfile, fitsfile
    ):
        self.skymodel = skymodel
        self.solarMS = solarMS
        self.calibratorMS = calibratorMS
        self.calibrator = calibrator
        self.sourcedb = sourcedb
        self.predictfile = predictfile
        self.applycalfile = applycalfile
        self.applybeamfile = applybeamfile
        self.configfile = configfile
        self.fitsfile = fitsfile

    ## Writes the values into a savefile
    def saveToSaveFile(self):
        configlines = self.readFileLines(self.configfile)
        predictlines = self.readFileLines(self.predictfile)
        applycallines = self.readFileLines(self.applycalfile)
        applybeamlines = self.readFileLines(self.applybeamfile)

        f = asksaveasfile(mode='w', defaultextension='.sav')
        if f is None: # If the dialog is closed with cancel then return nothing
            return

        f.write(self.skymodel + "\n")
        f.write(self.solarMS + "\n")
        f.write(self.calibratorMS + "\n")
        f.write(self.calibrator + "\n")
        f.write(self.sourcedb + "\n")
        f.write(self.fitsfile + "\n")

        f.write("\nPredict file contents:\n")
        for l in predictlines:
            f.write(l)

        f.write("\nApplycal file contents:\n")
        for l in applycallines:
            f.write(l)

        f.write("\nApplybeam file contents:\n")
        for l in applybeamlines:
            f.write(l)

        f.write("\nConfig file contents:\n")
        for l in configlines:
            f.write(l)

        f.close()

    ## Reads the lines from a file and returns them in a list
    def readFileLines(self, filename):
        retList = []
        try:
            file = open(filename)
            retList = [line for line in file.readlines() if line.strip()]
            file.close()
        except (OSError, IOError, KeyboardInterrupt):
            print("No config file present with the specified name, leaving the config file out of the save file\n")
            retList = []
            return retList
        return retList
