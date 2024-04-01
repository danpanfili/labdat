# LabDAT
Lab Data Analysis Toolkit: A modular framework for centralizing scientific data pipelines.

Run "main.py" to create SQLite database.

# Data Structure
Raw data is described using a key system, saved in database/keys.db

Pipeline expects the following file hierarchy:
>Experiment
>>Subject
>>>Run
>>>>Source

Example: /rawData/Experiment1/Subject1/Run1/EyeTracker

# Experiment
Each experiment needs a Load function which specifies how to load the trial information (see experiment/BerkeleyOutdoorWalk.py).

# Source
Each source needs a Load function which specifies the necessary file paths where data is stored. (see source/Pupil.py).

# Raw Data
Raw data is saved within the database as a blob (binary). This saves a large amount of space compared to csv representations.

These can be decoded in python using the np.frombuffer() function. C# code will also soon be provided.

Currently accepted filetypes: CSV
Soon to be added: mp4, npy

# Preprocessing
Coming soon...

# Experiment-unique processing
Coming soon...

# Analysis
Coming soon...

# Data Visualization
Coming soon...
