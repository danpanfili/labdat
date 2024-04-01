import os
import tools as t
from glob import glob

def LoadAll(run: list, module: str): 
    out = [[t.LoadFunction( f"{ module }.{ s }", 'Load')(r) for s in getattr(r,module).split(',') if t.LoadFunction( f"{ module }.{ s }", 'Load') is not None] for r in run]
    return t.Flatten(out)

class Raw:
    def __init__(self, info, key_delim='.'):
        self.source     = info['source']
        self.path       = info['path']
        self.name       = self.path.split('\\')[-1].split('.')[0]
        self.extension  = self.path.split('.')[-1]
        self.filetype   = t.GuessFiletype(self.path)
        self.key        = f"{info['run_key']}{key_delim}{key_delim.join([self.source, self.name])}" 
    
    def LoadAll(run: list): 
        return LoadAll(run, 'source')

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
    def __init__(self, val, key_delim = '.'):
        self.folder         = val[0]
        self.experiment     = self.folder.split('\\')[2]
        self.subject        = self.folder.split('\\')[3]
        self.run            = self.folder.split('\\')[4]
        self.source         = ','.join(val[1])
        self.key            = key_delim.join([self.experiment, self.subject, self.run])
    
    def LoadAll(path, slash_count = 4): return [Run(d) for d in os.walk(path) if d[0].count('\\') == slash_count]

class Database:
    global rawData_path
    rawData_path    = 'Z:\\rawdata\\'

    def __init__(self, db):
        self.db     = db

    def Load(self):
        self.run    = Run.LoadAll( rawData_path )
        self.trial  = Trial.LoadAll( self.run )
        self.raw    = Raw.LoadAll( self.run )

    def Update(self, load=False):
        if load: self.Load()
        self.db.Insert('run', self.run)
        self.db.Insert('trial', self.trial)
        self.db.Insert('raw', self.raw)