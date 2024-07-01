import os
import tools as t
from glob import glob
import numpy as np

def LoadAll(run: list, module: str): 
    out = [[t.LoadFunction( f"{ module }.{ s }", 'Load')(r) 
            for s in getattr(r,module).split(',') 
            if t.LoadFunction( f"{ module }.{ s }", 'Load') is not None] 
            for r in run]
    
    # out = [o for o in out if o != []]
    
    if type(out[0]) is list: out = t.Flatten(out)
    # out = np.array(out).flatten().tolist()
    
    return out

class Raw:
    def __init__(self, info, key_delim='.'):
        self.source     = info['source']
        self.path       = info['path']
        self.name       = self.path.split('\\')[-1].split('.')[0]
        self.extension  = self.path.split('.')[-1]
        self.filetype   = t.GuessFiletype(self.path)
        self.key        = f"{info['run_key']}{key_delim}{key_delim.join([self.source, self.name])}" 
    
    def LoadAll(run: list): return LoadAll(run, 'source')

class Trial:
    def __init__(self, info: dict, key_delim='.'):
        self.path           = info['path']
        self.id             = info['id']
        self.label          = str(info['label'][0])
        self.start_index    = int(info['index'][0])
        self.end_index      = int(info['index'][1])
        self.start_time     = float(info['time'][0])
        self.end_time       = float(info['time'][1])
        self.key            = f"{info['run_key']}{key_delim}{key_delim.join([str(self.id), self.label])}"

    def LoadAll(run: list): return LoadAll(run, 'experiment')

class Run:
    def __init__(self, val, key_delim = '.', slash_count = 5):
        self.folder         = val[0]
        self.experiment     = self.folder.split('\\')[slash_count - 2]
        self.subject        = self.folder.split('\\')[slash_count - 1]
        self.run            = self.folder.split('\\')[slash_count]
        self.source         = ','.join(val[1])
        self.key            = key_delim.join([self.experiment, self.subject, self.run])
    
    def LoadAll(path, slash_count = 5): return [Run(d) for d in os.walk(path) if d[0].count('\\') == slash_count]

class Database:
    def __init__(self, db, path):
        self.db     = db
        self.path   = path

    def Load(self):
        self.run    = Run.LoadAll( self.path )
        self.trial  = Trial.LoadAll( self.run )
        self.raw    = Raw.LoadAll( self.run )

    def Update(self, load=False):
        if load: self.Load()
        self.db.Insert('run', self.run)
        self.db.Insert('trial', self.trial)
        self.db.Insert('raw', self.raw)