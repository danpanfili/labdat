# LabDAT: Lab Data Analysis Toolkit
The labdat module is a toolkit for standardizing and centralizing data pipelines, specifically those which need to incorporate a variety of data streams. 

Version 0.0.1 - Initial Commit

Current Functionality:
* Key generation from raw data folder. 
    * 3 keys are made: Run (experiment_subject_run), Trial (trialNum_trialType), and Data (source_marker_dataType*_dataSubtype)
    * Currently only pulls data info from Motion Shadow ("Shadow") system.
    * Data subtype handling is fairly coarse, needs adjustment.

* Find data in raw data folders given run, trial, and data keys.
    * This process is slow, batching queries will be added to speed up this process.

* Data export to a CSV or Json
    * CSV ouputs a file with combined key header (run_key|trial_key|data_key) then populates the corresponding row with this data.
    * Json outputs a dict of key heirarchy (exp>sub>trialType>trialNum>source>marker>dataType>dataSubtype)
        * Dict creation process is very slow based on how the data finder is set-up, will be much faster after batching.

* General tools for data handling added (tools.py).
    * These are currently not very well organized, will adjust.
    * Some handlings are less than robust, particularly if we feed in arrays. May be best to make functions only take singular inputs, then handle arrays outside of tool function.

Things to do:
* Need to go through an automate the checks for experiment and source, then automatically go to submodule for run based on name. 
    * See how this was done in Load.Data with getattr()

* Need to add in interpolation mechanics, treating all data the same currently.
    * This should be done with SciPy interp options, just give method and params for each marker.

* We should also be checking if a database already exists before running, save multiples and can have a flag to redo a section and overwrite.

* SQLite database will be added.

* More data sources will be added.
    * First will be Pupil Core ("Pupil").

* Pre-processing scripts will be added.
    * First will be fixation finder and colmap sparse/dense reconstructions.

* Need to handle dependencies, notably CUDA and colmap stuff.
    * Conda environment for easy install?

* Main.py should be fragmented, too many classes.

* EVERY folder needs a README, EVERY function needs a help and basic documentation!