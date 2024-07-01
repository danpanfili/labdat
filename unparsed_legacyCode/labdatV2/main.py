#### LABDAT STAGING ######
import yaml

config_path = 'config.yml'


with open(config_path) as file: config = yaml.safe_load(file)

from InitializeDatabase import Main as InitDB
InitDB(config, config['stage'][0])

from UploadRawData import Main as UploadRaw
UploadRaw(config)


#### Docker file and dependencies #####

#### Input arguments ######

#### Parse keys and file information

#### Parse data and save in optimized format

#### Preprocess data from different streams

#### Integrate preprocessed data

#### Export preprocessed data

#### Visualize

print("Done!")