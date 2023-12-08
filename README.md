# LabDAT: Lab Data Analysis Toolkit
The labdat module is a toolkit for standardizing and centralizing data pipelines, specifically those which need to incorporate a variety of data streams. 

Version 0.0.1 - Initial Commit

Current Functionality:
1. Key generation from raw data folder. 
1. a. 3 keys are made: Run (experiment_subject_run), Trial (trialNum_trialType), and Data (source_marker_dataType*_dataSubtype)
1. b. Currently only pulls data info from Motion Shadow ("Shadow") system.
1. c. Data subtype handling is fairly coarse, needs adjustment.

2. Find data in raw data folders given run, trial, and data keys.
2. a. This process is slow, batching queries will be added to speed up this process.

3. Data export to a CSV or Json
3. a. CSV ouputs a file with combined key header (run_key|trial_key|data_key) then populates the corresponding row with this data.
3. b. Json outputs a dict of key heirarchy (exp>sub>trialType>trialNum>source>marker>dataType>dataSubtype)
3. b. i. Dict creation process is very slow based on how the data finder is set-up, will be much faster after batching.

4. General tools for data handling added (tools.py).
4. a. These are currently not very well organized, will adjust.
4. a. Some handlings are less than robust, particularly if we feed in arrays. May be best to make functions only take singular inputs, then handle arrays outside of tool function.

Things to do:
1. Need to go through an automate the checks for experiment and source, then automatically go to submodule for run based on name. 
1. a. See how this was done in Load.Data with getattr()

2. Need to add in interpolation mechanics, treating all data the same currently.
2. a. This should be done with SciPy interp options, just give method and params for each marker.

3. We should also be checking if a database already exists before running, save multiples and can have a flag to redo a section and overwrite.

4. SQLite database will be added.

5. More data sources will be added.
5. a. First will be Pupil Core ("Pupil").

6. Pre-processing scripts will be added.
6. a. First will be fixation finder and colmap sparse/dense reconstructions.

7. Need to handle dependencies, notably CUDA and colmap stuff.
7. a. Conda environment for easy install?

8. Main.py should be fragmented, too many classes.

9. EVERY folder needs a README, EVERY function needs a help and basic documentation!