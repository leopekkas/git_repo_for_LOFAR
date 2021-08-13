# LOFAR Imaging Tool - Usage instructions

## Starting the program

The LOFAR Imaging Tool (LIT) is designed to be used on the Kale cluster. The software is dependent on the following environments inside Kale:

1. A Sinteractive session when running the software outside of Kale’s head node
2. The singularity environment for accessing LOFAR functionalities
3. The LOFAR environment (included in the singularity environment)

First and foremost, a separate sinteractive session is needed to fire up the software as X11 forwarding is needed. For more information on activating a sinteractive session, refer to the HPC Corona guide.

Second step is specifying your environment to the singularity environment, which can be accessed with the following command:

`singularity run -B /proj /proj/group/corona/LofarPython/lofar_python_V0.9b.sif`

<div style="page-break-after: always;"></div>

This initializes singularity (version 0.9b) in your current working directory.
After initializing singularity the last step we need to do before starting up the imaging tool is simply to type in ``LOFAR``  into the terminal to specify we’re using the LOFAR environment and it’s functionalities.


## Files and the filesystem

The Imaging tool asks the user to input some files for imaging and plotting purposes. The files are used in the following ways:

Changing some of the files is done via a file dialog inside the program. Default file extensions the dialog looks for is specified inside the file dialog and can be changed (for instance changing the config file by default looks for a “.txt” file, but can be overwritten to search for files without an extension etc.)

#### Configuration file:

Contains information on all of the options on wsclean (number of cores, input MS name etc.) in the format ``[option]=[value]`` , where the value is an integer, double or a string type.
An example config file contains the following options (in whatever order):

1. cores
2. memory_limit
3. mgain
4. weight_briggs
5. size
6. size2
7. scale (an integer value, no need to specify asec)
8. polarisation (I, Q, U or V)
9. auto_mask
10. auto_threshold
11. data_column
12. n_iter
13. intervals_out
14. start_time
15. end_time

If all of the options are not specified or not used in wsclean, specify it under menu option “settings” -> “Manage the config file”. The program will also exclude options that are not specified in the configuration file or are mistyped.

####.fits file:

The selected .fits file which can be plotted via the “View” button.

####Solar MS:

The measurement dataset for the Sun.
The measurement set consists of a set ID and a subband. An example measurement set with an ID of L242124 and a subband of 160 would be called ``L242124_SB160_uv.dppp.MS``. Handling the measurement sets in the imaging tool is done by an ID input (string) and a subband input (integer).

If for some reason the MS file is in another format than the default, the user can change the “MS input format” option in the menu bar of the program.

####Calibrator MS:

Calibrator measurement dataset which is used in calibrating the Solar MS data via NDPPP commands. Make sure your calibrator MS has a matching subband to the Solar MS you’re working on.

####Calibrator name tag:

The “name tag” for our calibrator object. Check under the sourcedb input file what the calibrator abbreviation (TauAGG, VirA, CygA etc.) is in your skymodel data.

####Sourcedb input file:

A .skymodel file which specifies ???
Changing the sourcedb input file creates a new sourcedb output file.

#### Sourcedb output file:

<div style="page-break-after: always;"></div>

Informs which sourcedb is used for LOFAR’s ``NDPPP predict.parset`` command. A new sourcedb file can be created when a new sourcedb input file is specified.
The command functions in the same way as LOFAR’s command ``makesourcedb in=[input file] out=[output file]``.


## Commands

The following commands can be run inside the LOFAR imaging tool:

####NDPPP predict.parset

Builds a new predict.parset file for the data corresponding to the input information (Calibrator, Solar MS, Calibrator nametag) and runs LOFAR’s command ``NDPPP predict.parset`` which predicts things?

###NDPPP applycal.parset

Builds a new applycal.parset file for the data corresponding to the input information (Calibrator MS, Solar MS, Calibrator nametag) and runs LOFAR’s command ``NDPPP applycal.parset`` which applies calibrator?

####NDPPP applybeam.parset

Builds a new applybeam.parset file for the data corresponding to the input information (Calibrator MS, Solar MS, Calibrator nametag) and runs LOFAR’s command ``NDPPP applybeam.parset`` which produces a CORRECTED_DATA column into the Solar MS by doing ?

####wsclean

Runs the LOFAR command ``wsclean`` which produces the .fits files corresponding to the configuration options provided in the config file.
After the wsclean operation is complete, the terminal log text field will output the full command.
If the wsclean runs almost instantly and doesn’t produce any .fits files it may be because the specified data column is not found on the Solar MS file. Make sure you’ve specified the correct data column in your config file and that you have run the NDPPP commands for that file if needed.
If an error is encountered: check the output in the terminal log first to see if there’s maybe a typo in the configuration file and make sure you have LOFAR specified in the terminal before running the program.

####Run a coordinate transformation

####Plot & save multiple .fits files

<div style="page-break-after: always;"></div>

Used to save multiple .fits files at once. The command opens a file dialog where the user can [ctrl] + [click] multiple files to be saved. The saved plot will have a naming convention matching its .fits file.


##Making images with LOFAR data

Run the following steps to create plotted data from your chosen measurement sets and skymodel files:

<ol>
<li>Choose the right skymodel for the data set and the correct measurement sets</li>
<li>Run the needed calibration commands (NDPPP predict.parset etc.)</li>
<li>Run wsclean to make the .fits files with the config file information</li>
<li>Plot the image either by choosing a single .fits file and clicking the “View”</li>
button or by choosing “Plot & save multiple .fits files” and choosing the wanted .fits files</li>
<div style="page-break-after: always;"></div>
<li>Save the image with the plot window’s save functionality</li>
</ol>

##Example run (TL;DR)

To avoid reading this whole instruction sheet here’s an example on how to produce some data from some given files.
Let’s say you’re working with the following files:

1. Solar MS          :  L242126_SB160_uv.dppp.MS (ID = L242126, Subband = 160)
2. Calibrator MS  :  L242124_SB160_uv.dppp.MS (ID = L242124, Subband = 160, calibrator = Virgo A)
3. Skymodel file   :  Ateam_LBA_CC.skymodel.txt
4. Time interval    :  8/27/2014 13:20:00 - 13:30:30 (date depends on the MS file), produce 20 images/.fits files

A configuration file needs to be created for the files first, which tells what options our wsclean runs on.
An example config file is as follows:

``
cores=24
memory_limit=50
mgain=0.95
weight_briggs=0
size=1024
size2=1024
scale=10.5469
polarisation=I
auto_mask=7
auto_threshold=3
data_column=CORRECTED_DATA
n_iter=10
intervals_out=20
start_time=2014-08-27 13:20:00
end_time=2014-08-27 13:30:30
``

Where intervals_out tells how many .fits files will be produced and start_time/end_time tells what time periods the .fits files are created in between.
If you use time periods in the format in the example, make sure you have the “use datetime” option selected, the other option is to use integers matching to the datapoint number.

When you have the config file set up, start the program if it’s not open already, and choose your configuration file from the file dialog and specify the MS files via the “Change” button (ID = L242124/L242126, Subband = 160 in this case). Make sure your Solar MS and calibrator MS have matching subbands.

The calibrator name tag option can be found in your skymodel file (Ateam_LBA_CC.skymodel.txt in this case). Simply view the contents of the file and use the “Find a keyword” to locate an instance where your calibrator (Virgo A in this case) is used and see what nametag matches to that instance. (VirA / VirAGG etc.)

If you need to, run the NDPPP predict/applycal/applybeam options to your MS file via the command buttons. You can also run a job queue from the menu bar under the option “Command options / Run a job queue”

Now that your data is calibrated and stuff, run wsclean. If your configuration file is set up correctly, the command should take a good while and upon completion will print out to the terminal log the full command it just ran.
While running commands (especially longer ones) you should keep the terminal in which you started the Imaging tool on open and visible, to see the progression of the commands and to see if any errors are encountered (no errors should be thrown to the terminal but keep an eye out just in case).

The produced .fits files can be plotted and viewed with the “View/Change” buttons next to the chosen .fits file.
