import os, yaml, numpy, pandas, sqlite3, msgpack, glob, pyarrow.csv

def find_folders_at_depth(origin_folder, N):
    results = []
    
    for root, dirs, files in os.walk(origin_folder):
        rel_path = os.path.relpath(root, origin_folder)
        depth = len(rel_path.split(os.sep))
        
        if depth == N:
            results.append(root)
    
    return results

def find_subfolder_with_file(root_folder, filename):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if filename in filenames:
            return dirpath
    return False

def LoadConfigs(name, path = ""):
    cfg_path = glob.glob( os.path.join(path, 'cfg', name, "*.y*ml") )

    cfg = []
    for cp in cfg_path:
        with open(cp) as file:
            temp = yaml.safe_load(file)
            if 'dirname' not in temp.keys() or len(temp['dirname']) < 1:
                temp['dirname'] = temp['name']
            cfg.append(temp)

    return {c['dirname']:c for c in cfg}


def Main(config, stage):
    ## Initialization stuff
    if_exists = "replace" if stage.get('overwrite', False) else "append"
    
    if 'OUTPUT' not in config['dir'].keys() or not config['dir']['OUTPUT'] or len(config['dir']['OUTPUT']) < 1:
        config['dir']['OUTPUT'] = config['dir']['WORKSPACE']

    config['sources'] = LoadConfigs('source')
    config['experiments'] = LoadConfigs('experiment')

    ## For each experiment
    for experiment in config['experiments'].values():

        exp_folder = os.path.join(
            config['dir']['WORKSPACE'],
            stage['dir']['data'], 
            experiment['dirname'])

        ## Runs
        run_paths = find_folders_at_depth(exp_folder, experiment['hierarchy'].index('source')+1)
        run_info = [rp.split(os.sep)[-len(experiment['hierarchy']):] for rp in run_paths]
        run_key = ['_'.join(ri) for ri in run_info]

        runs = numpy.hstack([
            numpy.array(run_info), 
            numpy.array(run_paths)[:,numpy.newaxis], 
            numpy.array(run_key)[:,numpy.newaxis]])

        good_run = [ri[-1] in config['sources'].keys() for ri in run_info]
        runs = runs[good_run,:]

        ## Database
        df = pandas.DataFrame( runs, columns=experiment['hierarchy'] + ['path', 'key'] )

        db_path = os.path.join(
            config['dir']['OUTPUT'], 
            stage['dir']['database'], 
            f"{experiment['dirname']}.db")
        
        try:
            os.makedirs(os.path.join(config['dir']['OUTPUT'], stage['dir']['database']))
        except:
            print('Database directory already exists.')

        db = sqlite3.connect(db_path)
        df.to_sql('keys', db, if_exists=if_exists)
 
        ## Trials
        trials = []
        trial_fun = eval(experiment['trials']['build_function'])
        for run in runs:
            if not run[experiment['hierarchy'].index('source')] == experiment['trials']['source']:
                continue
            if not find_subfolder_with_file(run[-2], experiment['trials']['filename']):
                continue

            trial_path = os.path.join(run[-2], experiment['trials']['filename'])
            with open(trial_path, 'rb') as file:
                arr = msgpack.unpackb(file.read(), raw=False)
            trial_data = trial_fun(arr)

            for td in trial_data:
                td['key'] = run[-1]
            trials += trial_data

        trial_df = pandas.DataFrame(trials)
        trial_df.to_sql('trials', db, if_exists=if_exists)

    ## Import Test
    runs = df.query(f"subject in {config['settings']['SCOPE']['subject']}")

    for run in runs.iloc:
        if run['source'] not in config['sources']: continue

        for file in config['sources'][run['source']]['files']:
            if 'subfolder_contains' in file.keys(): 
                glob_path = glob.glob(os.path.join(run['path'],'**',file['subfolder_contains']), recursive=True)
                if len(glob_path) > 0:
                    path = glob.glob(os.path.join(run['path'],'**',file['subfolder_contains']), recursive=True)[0].replace(file['subfolder_contains'], file['filename'])
                else:
                    continue
            else:
                path = os.path.join(run['path'],file['filename'])

            if not os.path.exists(path): 
                continue

            if 'positions' in path: 
                print(f"Loading {file['filename']} for {run['key']}")

                alldat = pyarrow.csv.read_csv(path).to_pandas()
                if 'rename_vars' in file.keys():
                    alldat.rename(columns=file['rename_vars'])
                    # generics = {file['rename_vars']['default']col for col in df.columns if col not in file['rename_vars'].keys()}

                table = '_'.join([run['key'],file['filename']])
                alldat.to_sql(table, db, if_exists='replace')

    db.close()