import os, pandas
from keys import Trial

def Load(run, trial_file = 'annotations.csv'):
    folder = [d[0] for d in os.walk(run.folder) if trial_file in d[2]]

    if len(folder) != 1: return
    path = f'{folder[0]}\\{trial_file}'
    data = pandas.read_csv(path)

    label   = data.label.array.reshape((int) (data.label.array.__len__()/2), 2)
    index   = data.values[:,0].reshape((int) (data.index.array.__len__()/2), 2)
    time    = data.timestamp.array.reshape((int) (data.timestamp.array.__len__()/2), 2)

    return [Trial({
        'run_key': run.key,
        'path':    path,
        'id':      i,
        'label':   label[i,:],
        'index':   index[i,:],
        'time':    time[i,:]})
        for i,_ in enumerate(label)]