import pandas as pd, sqlite3, yaml, os, numpy as np, json
from glob import glob

# with open("poses.json") as file: poses = json.load(file)
# pos = np.array([pose['pos'] for pose in poses])

###############

rawData_path = 'Z:\\DataPipeline\\rawdata'

experiment_path = glob('experiment\\*.yaml')
source_path = glob('source\\*.yaml')

source = []
for sp in source_path:
    with open(sp) as file: 
        temp = yaml.safe_load(file)
        source.append(temp)
source_dir = [s['dirname'] for s in source]

#################
def find_folders_at_depth(origin_folder, N):
    results = []
    
    for root, dirs, files in os.walk(origin_folder):
        rel_path = os.path.relpath(root, origin_folder)
        depth = len(rel_path.split(os.sep))
        
        if depth == N:
            results.append(rel_path.split(os.sep))
    
    return results

#################

for exp_path in experiment_path:
    with open(exp_path) as file: experiment = yaml.safe_load(file)

    exp_folder = os.path.join(rawData_path, experiment['dirname'])
    hierarchy = experiment['hierarchy']

    folder_structure = find_folders_at_depth(exp_folder, hierarchy.index('source'))
    folder_structure = [[experiment['name']]+fs for fs in folder_structure]

    {}


    print()






filename = 'pupil_positions.csv'
path = fr'Z:\DataPipeline\rawdata\BerkeleyOutdoorWalk\Subject08\Binocular\Pupil\exports\002\{filename}'
chunksize = 10**5

exp_path = r'Z:\Panfili\labdat\source\Pupil.yaml'

def GetRenames(path = exp_path):
    with open(path) as file: src = yaml.safe_load(file)
    file_src = [f for f in src['files'] if f['filename'] == filename][0]
    if 'rename_vars' in file_src.keys(): 
        return file_src['rename_vars']
    else:
        return False

def ReadByChunks(path, chunksize = chunksize):
    dat = pd.read_csv(path, chunksize=chunksize, index_col=False)

    alldat = []
    for datchunk in dat:
        temp = datchunk
        alldat += [temp.copy()]
    alldat = pd.concat(alldat)

    return alldat

def RenameColumns(dataframe, renames):
    columns = dataframe.columns.to_list()
    names = {}
    for name,newname in renames.items():
        newnames = {c:c.replace(name, newname) for c in columns if c.startswith(name)}
        names.update(newnames)

    if 'default' in renames.keys():
        default = {c:f"{renames['default']}{c}" for c in columns if c not in names.keys()}
        names.update(default)

    dataframe = dataframe.rename(columns=names)
    return dataframe

alldat = ReadByChunks(path)
renames = GetRenames()
if renames != False:
    alldat = RenameColumns(alldat, renames)

# alldat[alldat['Frame.time'].between(1500,1600)]

table = filename.replace('.csv','')
conn = sqlite3.connect(f'{table}.db')
alldat.to_sql(table,conn)

print()