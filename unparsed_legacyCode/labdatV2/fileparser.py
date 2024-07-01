import pandas as pd, msgpack, io, json

chunksize = 10 ** 5

def GetRenames(source):
    if 'rename_vars' in source.keys(): 
        return source['rename_vars']
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

def CSV(path, source):
    alldat = ReadByChunks(path)
    renames = GetRenames(source)

    if renames != False:
        print('renaming...')
        alldat = RenameColumns(alldat, renames)

    return alldat

    # alldat[alldat['Frame.time'].between(1500,1600)]

def MP4(path):
    # Extract frames
    return

def XML(path):
    return pd.read_xml(path)

def MSGPACK(path):
    with open(path, 'rb') as file: 
        buf = json.dumps(msgpack.unpackb(file.read(), raw=False))
        out = pd.read_json(io.StringIO(buf))
    return out

def NPY(path):
    return

def parse(path, info):
    if 'filetype' not in info.keys() and '.' in path: 
        info['filetype'] = path.split('.')[-1]
    elif '.' not in path:
        return False
    
    if info['filetype'] == 'csv': return CSV(path, info)
    # if info['filetype'] == 'msgpack': return MSGPACK(path)