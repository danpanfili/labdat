import linecache
from collections import OrderedDict
import numpy as np

def Key2Path(key,delim="_"): #Replace all delims with \ for path conversion
    if isinstance(key, str): return key.replace(delim,"\\")
    return [k.replace(delim,"\\") for k in key]

def Key2Array(key,delim): #Return all unique values from each component of key
    if isinstance(key, str): return key.split(delim)
    array = []
    for i,c in enumerate(key[0].split(delim)): array.append(list(OrderedDict.fromkeys([k.split(delim)[i] for k in key])))
    return array

def Array2Key(array,delim): return delim.join(array) #Make a new key from array

def Contains(string, substring): #Does substring exist within string or array of strings
    if isinstance(string,str) and isinstance(substring,str): return string.find(substring)>-1 
    if isinstance(substring,str): return all([string.find(ss)>-1 for ss in substring])
    if isinstance(string,str): return all([s.find(substring)>-1 for s in string])
    return all(all(s.find(ss) > -1 for ss in substring) for s in string)

def Find(array,substring): return [val for val in array if Contains(val,substring)] #Returns strings in array that contain substring

def FindIndex(array,substring): return [index for index,val in enumerate(array) if Contains(val,substring)] #Returns indexes of strings in array that contain substring

def FindDict(dict,key=None,val=''): #Find all dicts with keys that contain key, and return array of values from them if provided
    if key is None: return [d[val] for d in dict]
    kk,kv = zip(*[[kk,kv] for kk, kv in key.items()])
    if val == '': return [d for d in dict if any([k==kk[0] and Contains(v,kv[0]) for k,v in d.items()])]
    return [d[val] for d in dict if any([{k:v}==key for k,v in d.items()])]

def GetLineCSV(path, trial_dict=None, data_dict=None): # This is currently only outputting strings, need to do type conversion somewhere
    if trial_dict is None: trial_dict = {'start_index':0,'end_index':None}
    
    if trial_dict['end_index'] is None:
        row_data = [linecache.getline(path,si).split(",") for si in trial_dict['start_index']]
    else: 
        row_index = [*range(trial_dict['start_index'],trial_dict['end_index'])]
        row_data = [linecache.getline(path,i).split(",") for i in row_index]

    if data_dict is None: return row_data
    return [row[data_dict['index']] for row in row_data]

class Time:
    def Interpolate(data=[],time=[],interval=.0):
        new_time = [time[0] + i * interval for i in range(int((time[-1] - time[0]) / interval) + 1)]
        if isinstance(data[0],list): return [np.interp(new_time,time,d) for d in data]
        return np.interp(new_time,time,data)

    def Nearest(data=[],time=[],interval=.0):
        new_time = [time[0] + i * interval for i in range(int((time[-1] - time[0]) / interval) + 1)]
        return
    # Almost certainly best to use scipy.interpolate functions here, don't rewrite the wheel

def ConstructNestedDict(dict_hierarchy,in_dict={},value=''):
    if len(dict_hierarchy) == 0: return in_dict
    if len(dict_hierarchy) == 1:
        if dict_hierarchy[0] not in in_dict:
            in_dict[dict_hierarchy[0]] = value
        return in_dict
    else:
        if dict_hierarchy[0] not in in_dict:
            in_dict[dict_hierarchy[0]] = {}
        ConstructNestedDict(dict_hierarchy[1:],in_dict[dict_hierarchy[0]],value)
        return in_dict
