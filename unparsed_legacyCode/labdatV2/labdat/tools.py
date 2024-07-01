import sys, importlib, filetype

def List2String(val,delim=','): return delim.join(val)
def Values(var):                return [f"'{val}'" for val in var.__dict__.values()]
def Keys(var):                  return [key for key in var.__dict__.keys()]
def NumKeys(var):               return len(var.__dict__.keys())
def Q(var):                     return ','.join(['?' for key in var.__dict__.keys()])
def Class2SQL(var):             return [tuple(v for v in va.__dict__.values()) for va in var]

def CommaString(var):           return ','.join(var)

def ImportAll(path, name):
    import importlib
    from glob import glob

    path = glob(fr'{path}\[!_]*.py')
    module = [p.replace('.py','').split('\\')[-1] for p in path]
    return [getattr(importlib.import_module(f'{name}.{m}'), m) for m in module]

def Flatten(arr): # Flattens arrays and removes and None elements
    out = []
    if type(arr) not in [list, tuple]: return arr
    if len(arr) == 1: return Flatten(arr[0])

    for a in arr:
        if a == None: continue
        out += a

    if any([type(o) is list or type(o) is tuple for o in out]): out = Flatten(out)

    return out

def GetCSVLine(file): return file.readline().replace(',\n','').replace('\n','').split(',')
def GetColumnType(col):
    try:
        col = float(col)
        return (float,8)
    except: return (str,2)

def LoadFunction(module, function):
    try:    
        importlib.import_module(module)
        module = sys.modules[module]
        return getattr(module, function)
    except: return None

def GuessFiletype(path):
    # Filetype guess
    try: guess = filetype.guess(path)
    except: return 'ERROR: No file at path.'
    if guess is not None: 
        return guess.extension
    
    try: 
        with open(path, 'r') as file: firstChar = file.read(1)
    except: return path.split('.')[-1]

    if firstChar == '{': return 'json'
    if firstChar == '<': return 'xml'
    return path.split('.')[-1]
