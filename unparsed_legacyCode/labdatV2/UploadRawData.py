import pandas as pd, numpy as np, os, sqlite3, yaml
from glob import glob
import fileparser as fp

chunksize = 10 ** 4

def find_subfolder_with_file(root_folder, filename):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if filename in filenames:
            return dirpath
    return False

def Main(config, overwrite = True):
    # experiment_db = glob(os.sep.join([config['workspace_path'], 'Database', '*.db']))
    # experiment_db.remove(experiment_db[1]) # temp fix
    experiment_db = ['Y:\\DataPipeline\Database\BerkeleyOutdoorWalk.db']

    for edb in experiment_db:
        conn = sqlite3.connect(edb)

        keys = pd.read_sql("SELECT * FROM keys", conn)
        trials = pd.read_sql("SELECT * FROM trials", conn)

        source_path = glob(os.sep.join(['Y:\\Panfili','labdat','source','*.yaml']))

        source = []
        for sp in source_path:
            with open(sp) as file: 
                temp = yaml.safe_load(file)
                source.append(temp)
        source_dir = [s['dirname'] for s in source]
        config['sources'] = {s['dirname']:s for s in source}
        sources = config['sources']
        col = keys.keys().to_list()

        for key in keys.values:
            key = {c:k for c,k in zip(col,key)}
            if key['source']=='Shadow':continue

            if key['key'] not in trials['key'].to_list() and key['key'].replace('Shadow','Pupil') not in trials['key'].to_list(): continue

            source = sources[key['source']]
            for source_file_info in source['files']:
                folder = key['path']
                if 'subfolder_contains' in source_file_info.keys():
                    folder = find_subfolder_with_file(key['path'], source_file_info['subfolder_contains'])
                if not folder: continue


                path = os.sep.join([folder, source_file_info['filename']])

                if '*' in path:
                    path = glob(path)

                    if len(path) < 1:
                        continue
                    else:
                        path = path[0]

                data = fp.parse(path, source_file_info)
                if data is False or data is None: continue
                print(path)

                # data.insert(len(data.columns),'source_key',key['key'],True)

                data.to_sql('_'.join([key['key'], source_file_info['filename']]), conn, if_exists='replace', chunksize=chunksize)
        conn.close()
    print()