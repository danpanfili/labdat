#### LABDAT STAGING ######
import yaml
from labdat import labdat as ld

config_path = 'config.yml'
with open(config_path) as file: 
    config = yaml.safe_load(file)

data = []

for stage in config['pipeline']:
    name = stage['stage']
    if stage['stage'] in ld.__dir__():
        data.append(getattr(ld, name).New(stage))
    else:
        print(f"ERROR: Couldn't find stage: {name}")

raw_db = ld.Database.New(config['pipeline'][0]) # Currently, passing this does nothing
raw_db.Initialize.Main(config, config['pipeline'][0])
raw_db.Import.Main(config, config['pipeline'][0])

# from InitializeDatabase import Main as InitDB
# InitDB(config, config['stages'][0])

# from UploadRawData import Main as UploadRaw
# UploadRaw(config)


#### Docker file and dependencies #####

#### Input arguments ######

#### Parse keys and file information

#### Parse data and save in optimized format

#### Preprocess data from different streams

#### Integrate preprocessed data

#### Export preprocessed data

#### Visualize

print("Done!")