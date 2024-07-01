# Lab Data Analysis Toolkit
LabDAT is a high-level library for processing experiment data. It simplifies and automates much of the pre-processing stages while enforcing standardized best-practices that allow for easy replication and extension of your pipeline. Built in functions for common raw data structures provide plug-and-play adaptation for most projects, and the modular framework allows for easy expansion to fit any need.

NOTE: In early development, major revisions will be made to both documentation and the codebase.
# Getting Started
## Configuration
LabDAT can function as a referenced library, or run as an automated pipeline using a config file (YAML, JSON, PICKLE).

### Directories
LabDAT requires an input and an output directory. If an output is not defined, it is assumed that to be the same as the input directory.

Additionally, you can provide locations for your custom configuration and script files. These will automatically be added to your LabDAT library for later use.
```yaml
dir:
  INPUT: /content/example/data
  OUTPUT: /content/example/output
  CONFIG: /content/example/cfg
  SCRIPTS: /content/example/scripts
```
### Global Settings
Various global settings can also be put in place. An important inclusion is CUDA availability and gpu index.

You can also give it a scope of what data you'd like to process, such as limiting by experiment or subject names. Note that these naming conventions must match you defined hierarchy for a dataset, as discussed in DATASET.
```yaml
settings:
  CUDA: yes
  GPU_INDEX: -1
  SCOPE:
    experiment: BerkeleyOutdoorWalk
    subject: [Subject08, Subject10]
```

### Defining a Pipeline
Here is where you list the functions you'd like to run on the data, defined by stages. The syntax matches how functions are called within the library, and can be nested.

For example:
```yaml
stage:
- Database:
    dir:
      data: raw
      database: database
      
    overwrite: true

    stage:
    - Initialize:
    - Upload:
```
Would be equivalent to:
```python
import labdat as ld

ld.Database.dir = {
  'data': 'raw',
  'database': 'database'
}
ld.Database.overwrite = True

ld.Database.Initialize()
ld.Database.Upload()
```

## Database
For efficient storage and access, LabDAT pulls raw data from known filetypes and stores them in a centralized SQLite database.

### Initialization
If you are starting from scratch, you will need to initialize a new database.

### Uploading
### Querying
## Preprocessing
## Analysis
## Visualization
