import os, yaml, numpy, pandas, sqlite3, msgpack, glob

# imports = ['os', 'yaml', 'sqlite3', 'msgpack']
# imports_as = {
#     'numpy':'numpy',
#     'pandas':'pandas'
# }

# for imp in imports: globals()[imp] = __import__(imp)
# for k,v in imports_as.items(): globals()[v] = __import__(k)

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

def Main(config, stage):
    if stage.get('overwrite', False):
        if_exists = "replace"
    else:
        if_exists = "append"

    # Assume the current working directory is the workspace
    data_path = fr'Z:\DataPipeline\rawdata'
    workspace_path = config['dir']['OUTPUT']
    cfg = f'{os.getcwd()}\\labdat\\cfg'

    # Use the 'folder' key from the YAML for the database directory
    database_dir = os.path.join(workspace_path, stage['folder'])
    
    # Use the 'data' key from the YAML for the raw data directory
    rawData_path = os.path.join(workspace_path, stage['data'])

    CWD = os.getcwd()

    experiment_path = glob.glob(os.path.join(cfg, 'labdat', 'experiment', '*.yaml'))
    source_path = glob.glob(os.path.join(cfg, 'labdat', 'source', '*.yaml'))

    source = []
    for sp in source_path:
        with open(sp) as file:
            temp = yaml.safe_load(file)
            source.append(temp)
    source_dir = [s['dirname'] for s in source]
    config['sources'] = {s['dirname']:s for s in source}

    config['experiments'] = []

    for exp_path in experiment_path:
        with open(exp_path) as file:
            experiment = yaml.safe_load(file)

        exp_folder = os.path.join(rawData_path, experiment['dirname'])
        hierarchy = experiment['hierarchy']

        run_paths = numpy.array(find_folders_at_depth(exp_folder, hierarchy.index('source')+1))
        run_info = numpy.array([rp.split(os.sep)[-len(hierarchy):] for rp in run_paths])
        run_key = numpy.array(['_'.join(ri) for ri in run_info])

        runs = numpy.hstack([run_info, run_paths[:,numpy.newaxis], run_key[:,numpy.newaxis]])

        good_run = [ri[-1] in source_dir for ri in run_info]
        runs = runs[good_run,:]

        df = pandas.DataFrame(runs, columns=hierarchy + ['path'] + ['key'])

        db_path = os.path.join(database_dir, f"{experiment['dirname']}.db")
        db = sqlite3.connect(db_path)
        df.to_sql('keys', db, if_exists=if_exists)

        trials = []
        for run in runs:
            if not run[hierarchy.index('source')] == experiment['trials']['source']:
                continue
            if not find_subfolder_with_file(run[-2], experiment['trials']['filename']):
                continue

            trial_path = os.path.join(run[-2], experiment['trials']['filename'])
            with open(trial_path, 'rb') as file:
                arr = msgpack.unpackb(file.read(), raw=False)
            trial_data = eval(experiment['trials']['build_function'])

            for td in trial_data:
                td['key'] = run[-1]
            trials += trial_data

        trial_df = pandas.DataFrame(trials)
        trial_df.to_sql('trials', db, if_exists=if_exists)
        db.close()

        