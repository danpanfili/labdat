import time, pandas
import numpy as np
import database as db
import tools as t

class Data:
    def __init__(self, info):
        self.source     = info['source']['source']
        self.name       = info['name']
        self.dtype      = info['values'].dtype.name
        self.encoding   = info['values'].dtype.str
        self.itemsize   = info['values'].itemsize
        self.size       = info['values'].size
        self.data       = info['values'].tobytes()
        self.key        = f"{ info['source']['key'] }.{ self.name }"

    class Load:
        def Video(dataKey):
            return
        
        def CSV(dataKey, subfolder = 'raw', overwrite = False):
            start_time  = time.time()

            experiment  = dataKey['key'].split('.')[0]
            table       = '.'.join(dataKey['key'].split('.')[0:3])
            target_db   = db.Database( experiment, fr"{db.Database.path}\{subfolder}" )

            # Simple overwrite function, check if key exists in table, skip if so
            if not overwrite and table in target_db.Tables():
                if target_db.Get(table, column= 'key', listRows= True, filter= f'key GLOB "{dataKey["key"]}*"')['key'] != []: return

            csv_data    = pandas.read_csv(dataKey['path'])

            with open(dataKey['path'], 'r') as file: header = t.GetCSVLine(file)

            for h in header:
                print('\x1b[1A\n' + f"Elapsed: {round(time.time() - start_time, 3)} seconds.", end = '' )

                rename = t.LoadFunction(f"source.{dataKey['source']}", 'Rename')
                if rename is None:  name = h
                else:               name = rename(h, dataKey['key'])

                values = csv_data[h].to_numpy()
                if len(values) == 0: continue
                if values[0]==values[-1]:
                    if(np.unique(values).size == 1): values = np.unique(values)

                data = Data({
                    'name':     name,
                    'values':   values,
                    'source':   dataKey })
                
                target_db.Insert(table, [data])

            print('\x1b[1A\n' + f"Done in: {round(time.time() - start_time, 3)} seconds.      ")

        def mp4(): return # Need to use ffmpeg for lossless compression
        def json(): return
        def xml(): return