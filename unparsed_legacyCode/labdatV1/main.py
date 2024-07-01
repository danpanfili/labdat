import sys
from database import Database as db
import keys, data
import numpy as np
np.set_printoptions(2)

rawData_path = 'Z:\\DataPipeline\\rawdata\\'

overwrite = False

##########################################
key = keys.Database( db('keys'), rawData_path )
key.Update(True)

##########################################
# raw_csvs = key.db.Get(table= 'raw', filter= ["filetype='csv'", "source='Pupil'"])
raw_csvs = key.db.Get(table= 'raw', filter="filetype='csv'")
for i, csv in enumerate(raw_csvs):
    print(f"\nLoading {i+1} of {len(raw_csvs)}, csv from: {csv['key']}")

    data.Data.Load.CSV(csv, 'raw', overwrite)
############################################

sys.path.append(r'Z:\DataPipeline\analysis')

import BerkeleyOutdoorWalk.main as bow
bow.Test(db)

############################################

print('Done')
